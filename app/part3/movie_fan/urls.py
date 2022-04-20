from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_page, name='home_page'),
    path('login/', views.login, name='login'),
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
    path('add_rating_1/', views.add_rating_1, name='add_rating_1'),
    path('add_rating_2/', views.add_rating_2, name='add_rating_2'),
    path('add_rating_3/', views.add_rating_3, name='add_rating_3'),
    path('add_rating_4/', views.add_rating_4, name='add_rating_4'),
    path('add_rating_5/', views.add_rating_5, name='add_rating_5'),
    path('rent/', views.rent, name='rent'),
    path('rent_confirm/', views.rent_confirm, name='rent_confirm'),
    path('mark_unwatched/', views.mark_unwatched, name='mark_unwatched'),
    path('popular_actors/', views.popular_actors, name='popular_actors'),
    path('popular_directors/', views.popular_directors, name='popular_directors'),
]
