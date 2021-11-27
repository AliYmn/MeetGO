from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.shortcuts import redirect
from .models import Profile
from django.core.files.storage import FileSystemStorage

def homePage(request):
    return render(request,'index.html')

def meetingDetails(request):
    return render(request,'details.html')

def exploreMeetings(request):
    return render(request,'explore.html')

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

def create(request):
    return render(request,'create.html')

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