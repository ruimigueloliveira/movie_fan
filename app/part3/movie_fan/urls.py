from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_page, name='home_page'),
    path('signup/', views.signup, name='signup'),
    path('signup_confirm/', views.signup_confirm, name='signup_confirm'),
    path('serieslist/', views.serieslist, name='serieslist'),
    path('movieslist/', views.movieslist, name='movieslist'),
    path('movie/', views.movie, name='movie'),
    path('actor/', views.actor, name='actor'),
    path('director/', views.director, name='director'),
    path('country/', views.country, name='country'),
    path('category/', views.category, name='category'),
    path('search/', views.search, name='search'),
    path('rent/', views.rent, name='rent'),
    path('rent_confirm/', views.rent_confirm, name='rent_confirm'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login, name='login'),
    path('login_confirm/', views.login_confirm, name='login_confirm'),
]
