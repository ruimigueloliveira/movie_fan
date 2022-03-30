"""djangoProject2 URL Configuration

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
    path('filme/', views.filme, name='filme'),
    path('movieslist/', views.movieslist, name='movieslist'),
    path('serieslist/', views.serieslist, name='serieslist'),
    path('program_from_country/<country>/', views.program_from_country, name='program_from_country'),
    path('program_from_country/', views.home_page, name='program_from_country'),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('userprofile/', views.userprofile, name='userprofile'),
    path('has_watched/', views.has_watched, name='has_watched'),
    path('has_not_watched/', views.has_not_watched, name='has_not_watched'),
    path('delete_movie/', views.delete_movie, name='delete_movie'),
    path('add_rating_1/', views.add_rating_1, name='add_rating_1'),
    path('add_rating_2/', views.add_rating_2, name='add_rating_2'),
    path('add_rating_3/', views.add_rating_3, name='add_rating_3'),
    path('add_rating_4/', views.add_rating_4, name='add_rating_4'),
    path('add_rating_5/', views.add_rating_5, name='add_rating_5'),
    path('verify_xml/', views.verify_xml, name='verify_xml'),
    path('news/', views.news, name='news')
]
