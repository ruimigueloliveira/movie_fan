"""webproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
    path('', views.home, name='home'),
    path('nmovies/', views.nmovies, name='nmovies'),
    path('movie/', views.movie, name='movie'),
    path('movie/id', views.id, name='id'),
    path('movie/type', views.type, name='type'),
    path('movie/title', views.title, name='title'),
    path('movie/director', views.director, name='director'),
    path('movie/cast', views.cast, name='cast'),
    path('movie/country', views.country, name='country'),
    path('movie/date_added', views.date_added, name='date_added'), 
    path('movie/release_year', views.release_year, name='release_year'),
    path('movie/rating', views.rating, name='rating'),
    path('movie/duration', views.duration, name='duration'),
    path('movie/listed_in', views.listed_in, name='listed_in'),
    path('movie/description', views.description, name='description'),
]
