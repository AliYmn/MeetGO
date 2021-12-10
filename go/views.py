from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect
from .models import Profile,Category,Events
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_datetime
from django.views.generic import ListView

def homePage(request):
    category_list = Category.objects.all()
    meetings = Events.objects.all().order_by("-start_time")[:2]
    return render(request,'index.html',{
        "category_list":category_list,
        "meetings":meetings,
    })

@login_required(login_url='/login/')
def meetingDetails(request,pk,url):
    event = Events.objects.get(id=pk,url=url)
    return render(request,'details.html',{
        "event":event,
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
            Events.objects.create(
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
            return render(request,'create.html',{"category_list":category_list,"success":True})
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
    return render(request,'profile.html',{
        "about":about,
        "link":link
    })

def logout_user(request):
    logout(request)
    return redirect("/")