"""sudokuX URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name="home"),
    path('signup/',views.signupuser,name='signupuser'),
    path('logout/',views.logoutuser,name='logoutuser'),
    path('login/',views.loginuser,name='loginuser'), 
    #path('',views.showSudoku),
    path('newgame/',views.newGame,name='newgame'),
    path('startgame/',views.showSudoku,name='startgame'),
    path('result/',views.result,name='result'),
    path('records/',views.records,name='records'),
    path('developercontacts/',views.developercontacts,name='developercontacts'),
    path('howtoplay/',views.howtoplay,name='howtoplay'),
]
