"""first_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
#from django.conf.urls import include
from first_app import views
urlpatterns = [
    #path('',views.index,name ='index'),
    #path('first_app/',include('first_app.urls')),
    #('helpPage/',include('first_app.urls')),
    path('',views.index,name='index'),
    #path('formpage/',views.form_name_view,name='form_name'),
    path('restaurantPage/',views.restaurantPage,name='restaurant'),
    path('moviePage/',views.moviePage,name='movie'),
    path('inputReview',views.inputFormReview,name='inputForm'),
    path('admin/', admin.site.urls),
    path('nowPlaying/', views.myNowPlayingbuttonPost, name='myNowPlayingbuttonPost'),
     path('popular/', views.myPopularbuttonPost, name='myPopularbuttonPost'),
    #path('geolocation/',views.geolocation,name='geolocation')
]
