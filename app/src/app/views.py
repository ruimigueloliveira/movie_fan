import email
from django.http import Http404
from django.shortcuts import render
import requests
from django.shortcuts import render
from .forms import myRentalForms, mySignUpForms, myLogInForms
import numpy as np

username = ""
email = ""
password = ""

# Home Page
def home_page(request):
    tparams = {
        'username': username,
    }
    return render(request, 'home_page.html', tparams)

# Sign Up
def signup(request):
    tparams = {
        'username': username,
    }
    return render(request, 'signup.html', tparams)

# Sign Up Confirm
def signup_confirm(request):
    form = mySignUpForms(request.POST)
    data = {}
    if form.is_valid():
        data = form.cleaned_data

    response = requests.post(
        f"http://localhost:8001/deti-egs-moviefan/Authentication/1.0.0/v1/signup",
        json=dict(username=data["username"], email=data["email"], password=data["password"])
    )

    global username
    username = data["username"]

    status = response.json()["status"]

    if (response.status_code != 200) or ("OK" not in response.text):
        username = ""

    tparams = {
        'username': username,
        'status' : status
    }

    return render(request, 'signup_confirm.html', tparams)

# login_step_1
def login(request):
    tparams = {
        'username': username,
    }
    return render(request, 'login.html', tparams)

# login_step_2
def login_confirm(request):
    form = myLogInForms(request.POST)
    data = {}
    if form.is_valid():
        data = form.cleaned_data

    response = requests.post(
        f"http://localhost:8001/deti-egs-moviefan/Authentication/1.0.0/v1/auth-token",
        json=dict(username=data["username"], password=data["password"])
    )

    global username
    username = data["username"]

    status = response.json()["status"]

    if (response.status_code != 200) or ("OK" not in response.text):
        username = ""
    
    tparams = {
        'username': username,
        'status' : status
    }

    return render(request, 'login_confirm.html', tparams)

# login_step_1
def logout(request):
    global username
    bye_user = username
    username = ""
    global email
    email = ""
    global password
    password = ""

    tparams = {
        'username': username,
        'bye_user' : bye_user
    }
    return render(request, 'logout.html', tparams)

# Profile
def profile(request):
    user_rentals = requests.get("http://127.0.0.1:8002/rentals/rental/v1/productsBy/"+username).json()
    tparams = {
        'username': username,
        'user_rentals': user_rentals
    }
    return render(request, 'profile.html', tparams)

# List of all the movies
def movieslist(request):
    allmovies_ditc = requests.get("http://127.0.0.1:8003/v1/shows?type=movie").json()
    tparams = {
        'allmovies_ditc': allmovies_ditc,
        'username': username,
    }
    return render(request, 'list_of_movies.html', tparams)

# Information about the movie/serie
def movie(request):
    if not 'id' in request.GET:
        raise Http404("Filme não disponível!")
    id = request.GET['id']
    movie_ditc = requests.get("http://127.0.0.1:8003/v1/movie/?show_id="+id).json()
    tparams = {
        'movie': movie_ditc,
        'username': username,
    }
    return render(request, 'program_info.html', tparams)

# List of all the series
def serieslist(request):
    allseries_ditc = requests.get("http://127.0.0.1:8003/v1/shows?type=tvshow").json()
    tparams = {
        'allseries_ditc': allseries_ditc,
        'username': username,
    }
    return render(request, 'list_of_series.html', tparams)

# Rent Movie
def rent(request):
    if not 'id' in request.GET:
        raise Http404("Filme não disponível!")
    id = request.GET['id']
    movie_statistics = requests.get("http://127.0.0.1:8003/v1/movie/?show_id="+id).json()
    tparams = {
        'movie_statistics': movie_statistics,
        'username': username
    }
    return render(request, 'rent.html', tparams)

# Confirm Rent Movie
def rent_confirm(request): 
    if not 'id' in request.GET:
        raise Http404("Filme não disponível!")
    id = request.GET['id']
    form = myRentalForms(request.POST)
    data = {}
    if form.is_valid():
        data = form.cleaned_data
    movie_title = requests.get("http://127.0.0.1:8003/v1/movie/?show_id="+id).json()["title"]
    movie_price = round(np.log(int(data["rental_time"])+1),2)*2
    movie_data = {"price": movie_price, "entity": "movie_fan", "username": username, "title": movie_title, "rental_time": data["rental_time"]}
    requests.post("http://127.0.0.1:8002/rentals/rental/v1/products/"+id, data = movie_data)
    tparams = {
        'movie_data' : movie_data,
        'username': username,
    }
    return render(request, 'rent_confirm.html', tparams)

# Lists all movies/series of an actor
def actor(request):
    tparams = {
        'username': username,
    }
    return render(request, 'actor.html', tparams)

# Lists all movies/series of a director
def director(request):
    tparams = {
        'username': username,
    }
    return render(request, 'director.html', tparams)

# Lists all movies/series directed in a country
def country(request):
    tparams = {
        'username': username,
    }
    return render(request, 'country.html', tparams)

# Lists all movies/series from a category (action, drama, comedy, etc.)
def category(request):
    tparams = {
        'username': username,
    }
    return render(request, 'category.html', tparams)

# Searches for movies from the name, actors or countries
def search(request):
    tparams = {
        'username': username,
    }
    return render(request, 'search.html', tparams)
