"""MeetGO URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from go.views import homePage,exploreMeetings,meetingDetails,register,loginUser,create,profile,logout_user,profile_details
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homePage),
    path('event/<int:pk>/<str:url>/', meetingDetails),
    path('explore/', exploreMeetings.as_view()),
    path('register/', register),
    path('login/', loginUser),
    path('create/', create),
    path('profile/', profile),
    path('logout/',logout_user),
    path('profile/<int:pk>',profile_details)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
