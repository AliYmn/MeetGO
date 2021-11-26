from django.shortcuts import render

def homePage(request):
    return render(request,'index.html')

def meetingDetails(request):
    return render(request,'details.html')

def exploreMeetings(request):
    return render(request,'explore.html')

def register(request):
    return render(request,'register.html')

def login(request):
    return render(request,'login.html')

def create(request):
    return render(request,'create.html')