"""edc_project2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
    path('', views.home_page, name='home_page'),
    path('serieslist/', views.serieslist, name='serieslist'),
    path('movieslist/', views.movieslist, name='movieslist'),
    path('movie/', views.movie, name='movie'),
    path('actor/', views.actor, name='actor'),
    path('director/', views.director, name='director'),
    path('country/', views.country, name='country'),
    path('category/', views.category, name='category'),
    path('search/', views.search, name='search'),
    path('add_rating_1/', views.add_rating_1, name='add_rating_1'),
    path('add_rating_2/', views.add_rating_2, name='add_rating_2'),
    path('add_rating_3/', views.add_rating_3, name='add_rating_3'),
    path('add_rating_4/', views.add_rating_4, name='add_rating_4'),
    path('add_rating_5/', views.add_rating_5, name='add_rating_5'),
    path('mark_watched/', views.mark_watched, name='mark_watched'),
    path('mark_unwatched/', views.mark_unwatched, name='mark_unwatched'),
    path('popular_actors/', views.popular_actors, name='popular_actors'),
    path('popular_directors/', views.popular_directors, name='popular_directors'),
]
