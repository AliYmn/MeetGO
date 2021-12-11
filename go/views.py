from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect
from .models import Profile,Category,Events,Follow,Subscription,Notifications
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_datetime
from django.views.generic import ListView
from datetime import datetime, timedelta
from django.utils import timezone


def homePage(request):
    category_list = Category.objects.all()
    meetings = Events.objects.all().order_by("-start_time")[:2]
    one_week_ago = datetime.today() - timedelta(days=7)
    notif_count = Notifications.objects.filter(targetuser=request.user,start_time__gte=one_week_ago).count()
    return render(request,'index.html',{
        "category_list":category_list,
        "meetings":meetings,
        "notif_count":notif_count
    })

@login_required(login_url='/login/')
def meetingDetails(request,pk,url):
    event = Events.objects.get(id=pk,url=url)
    check = Events.objects.filter(id=pk,url=url,user=request.user).exists()
    follow = Follow.objects.filter(event=event)
    check_follow = Follow.objects.filter(event=event,user=request.user).exists()
    profile = Profile.objects.get(user=event.user)
    check_sub = Subscription.objects.filter(organizer=profile,user=request.user).exists()
    return render(request,'details.html',{
        "event":event,
        "check":check,
        "follow":follow,
        "check_follow":check_follow,
        "check_sub":check_sub
    })

class exploreMeetings(ListView):
    model = Events
    queryset = Events.objects.filter().order_by('-start_time')
    context_object_name = 'events'
    template_name = 'explore.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super(exploreMeetings, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        return context

def register(request):
    # register user
    if request.method == "POST":
        # print("request.POST",request.POST)
        try:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            repassword = request.POST['repassword']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
        except:
            return render(request,'register.html',{
                "empty":True,
            })
        if 'check' not in request.POST:
            return render(request,'register.html',{
                "error":True,
            })
        else:
            check = request.POST['check']
        if check != "on":
            return render(request,'register.html',{
                "error":True,
            })
        if password != repassword:
            return render(request,'register.html',{
                "notsame":True,
            }) 
        # register user here no error
        new_user = User.objects.create_user(
            username,email,password
        )
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.save()

        # create profile
        Profile.objects.create(
            user = new_user,
            description = "",
            url = "",
        )

        return render(request,'register.html',{"success":True})
    return render(request,'register.html')

def loginUser(request):
    if request.method == "POST":
        # print(request.POST)
        if 'email' in request.POST and "password" in request.POST:
            email = request.POST['email']
            password = request.POST['password']
            try:
                username = User.objects.get(email=email).username
                user = authenticate(username=username, password=password)
            except:
                  return render(request,'login.html',{"not_user":True})
            if user is not None:
                login(request,user)
            else:
                return render(request,'login.html',{"not_user":True})
        else:
            return render(request,'login.html',{"error":True})

        return redirect("/")
    return render(request,'login.html')

@login_required(login_url='/login/')
def create(request):
    category_list = Category.objects.all()
    if request.method == "POST": 
        try:
            title = request.POST.get("title")
            date = request.POST.get("date")
            description = request.POST.get("description")
            event_type = request.POST.get("event_type")
            category = request.POST.get("category")
            address = request.POST.get("address")
            keywords = request.POST.get("keywords")
            myfile = request.FILES['file']
            fs = FileSystemStorage()
            file_name = fs.save(myfile.name,myfile)
            url = fs.url(file_name)
            event = Events.objects.create(
                user=request.user,
                title=title,
                event_type=event_type,
                tags=keywords,
                image = url,
                category_list = Category.objects.get(title=category),
                description=description,
                start_time=parse_datetime(date),
                address=address,
            )
            subs = Subscription.objects.filter(organizer__user__in=[request.user])
            print('subs: ', subs)
            for s in subs:
                Notifications.objects.create(
                    title="Event Created",
                    fromuser=request.user,
                    targetuser=s.user,
                    event=event
                )
            return render(request,'create.html',{"category_list":category_list,
            "success":True,
            "event_id":event.id,
            "event_url":event.url
            })
        except:
            return render(request,'create.html',{"category_list":category_list,"error":True})
    category_list = Category.objects.all()
    return render(request,'create.html',{"category_list":category_list})

@login_required(login_url='/login/')
def profile(request):
    if request.method == "POST":
        try:
            myfile = request.FILES['file']
            fs = FileSystemStorage()
            file_name = fs.save(myfile.name,myfile)
            url = fs.url(file_name)
            Profile.objects.filter(user=request.user).update(
                description = request.POST["about"],
                url=url
            )
        except:
              Profile.objects.filter(user=request.user).update(
                description = request.POST["about"],
            )
    about = Profile.objects.get(user=request.user).description
    link = Profile.objects.get(user=request.user).url
    follow = Follow.objects.filter(user=request.user)
    subs = Subscription.objects.filter(user=request.user)
    events = Events.objects.filter(user=request.user)
    return render(request,'profile.html',{
        "about":about,
        "link":link,
        "follow":follow,
        "subs":subs,
        "events":events
    })

def logout_user(request):
    logout(request)
    return redirect("/")


@login_required(login_url='/login/')
def profile_details(request,pk):
    user = User.objects.get(pk=pk)
    about = Profile.objects.get(user=user).description
    link = Profile.objects.get(user=user).url
    follow = Follow.objects.filter(user=user)
    subs = Subscription.objects.filter(user=user)
    events = Events.objects.filter(user=user)
    return render(request,'profile_details.html',{
        "about":about,
        "link":link,
        "follow":follow,
        "subs":subs,
        "events":events
    })


@login_required(login_url='/login/')
def followup(request,pk):
    event = Events.objects.filter(id=pk)
    user = request.user
    follow = Follow.objects.filter(user=user)
    # if exists add event
    if follow.exists():
        follow_get = Follow.objects.get(user=user)
        obj = follow_get.event.add(*event)

    # if not exists create object and add event
    if not follow.exists():
        Follow.objects.create(
            user = user
        )
        follow_get = Follow.objects.get(user=user)
        obj = follow_get.event.add(*event)

    get_event = Events.objects.get(id=pk)
    return redirect("/event/"+str(get_event.pk)+"/"+str(get_event.url)+"/")


@login_required(login_url='/login/')
def unfollow(request,pk):
    event = Events.objects.get(id=pk)
    user = request.user
    follow = Follow.objects.get(user=user,event=event)
    follow.event.remove(event)
    return redirect("/event/"+str(event.pk)+"/"+str(event.url)+"/")


@login_required(login_url='/login/')
def subup(request,pk):
    event = Events.objects.get(id=pk)
    profile = Profile.objects.filter(user=event.user)
    user = request.user
    subs = Subscription.objects.filter(user=user)
    # if exists add event
    if subs.exists():
        subs_get = Subscription.objects.get(user=user)
        obj = subs_get.organizer.add(*profile)

    # if not exists create object and add event
    if not subs.exists():
        Subscription.objects.create(
            user = user
        )
        subs_get = Subscription.objects.get(user=user)
        obj = subs_get.organizer.add(*profile)

    return redirect("/event/"+str(event.pk)+"/"+str(event.url)+"/")


@login_required(login_url='/login/')
def unsubs(request,pk):
    event = Events.objects.get(id=pk)
    profile = Profile.objects.get(user=event.user)
    user = request.user
    subs = Subscription.objects.get(user=user)
    subs.organizer.remove(profile)
    return redirect("/event/"+str(event.pk)+"/"+str(event.url)+"/")

@login_required(login_url='/login/')
def notifications(request):
    about = Profile.objects.get(user=request.user).description
    link = Profile.objects.get(user=request.user).url
    notif = Notifications.objects.filter(targetuser=request.user)
    return render(request,'notifications.html',{
        "about":about,
        "link":link,
        "notif":notif
    })