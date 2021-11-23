from django.shortcuts import render

def homePage(request):
    return render(request,'index.html')

def meetingDetails(request):
    return render(request,'details.html')

def exploreMeetings(request):
    return render(request,'explore.html')