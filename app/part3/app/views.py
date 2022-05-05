import email
from django.http import Http404
from django.shortcuts import render
import requests
from django.shortcuts import render
from .forms import myRentalForms, mySignUpForms, myLogInForms
import numpy as np

username = "admin1"
email = "admin1@it.org"
password = "admin1Pa$$"

# Home Page
def home_page(request):
    return render(request, 'home_page.html')

# Sign Up
def signup(request):
    return render(request, 'signup.html')

# Sign Up Confirm
def signup_confirm(request):
    form = mySignUpForms(request.POST)
    data = {}
    if form.is_valid():
        data = form.cleaned_data

    global username
    username = data["username"]
    global email
    email = data["email"]
    global password
    password = data["password"]

    response = requests.post(
        f"http://localhost:8001/deti-egs-moviefan/Authentication/1.0.0/v1/signup",
        json=dict(username=username, email=email, password=password)
    )
    error = False
    if response.status_code != 200:
        error = True
    if "OK" not in response.text:
        error = True
    tparams = {
        'username': data["username"],
        'error' : error,
        'response' : response.text
    }
    return render(request, 'signup_confirm.html', tparams)

# Login
def login(request):
    return render(request, 'login.html')

# Log In Confirm
def login_confirm(request):
    form = myLogInForms(request.POST)
    data = {}
    if form.is_valid():
        data = form.cleaned_data
    
    global username
    username = data["username"]
    global email
    email = data["email"]
    global password
    password = data["password"]

    response = requests.post(
        f"http://localhost:8001/deti-egs-moviefan/Authentication/1.0.0/v1/auth-token",
        json=dict(username=username, email=email, password=password)
    )
    print('\nResponse body is : ' + response.text)

    error = False
    if response.status_code != 200:
        error = True
    if "OK" not in response.text:
        error = True
        
    tparams = {
        'username': data["username"],
        'error' : error,
        'response' : response.text
    }

    return render(request, 'login_confirm.html', tparams)

# Profile
def profile(request):
    user_rentals = requests.get("http://127.0.0.1:8002/rentals/rental/v1/productsBy/"+username).json()
    tparams = {
        'username': username,
        'email': email,
        'password': password,
        'user_rentals': user_rentals
    }
    return render(request, 'profile.html', tparams)

# List of all the movies
def movieslist(request):
    allmovies_ditc = requests.get("http://127.0.0.1:8003/v1/shows?type=movie").json()
    tparams = {
        'allmovies_ditc': allmovies_ditc
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
    }
    return render(request, 'program_info.html', tparams)

# List of all the series
def serieslist(request):
    allseries_ditc = requests.get("http://127.0.0.1:8003/v1/shows?type=tvshow").json()
    tparams = {
        'allseries_ditc': allseries_ditc
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
        'movie_data' : movie_data
    }
    return render(request, 'rent_confirm.html', tparams)

# Lists all movies/series of an actor
def actor(request):
    return render(request, 'actor.html')

# Lists all movies/series of a director
def director(request):
    return render(request, 'director.html')

# Lists all movies/series directed in a country
def country(request):
    return render(request, 'country.html')

# Lists all movies/series from a category (action, drama, comedy, etc.)
def category(request):
    return render(request, 'category.html')

# Searches for movies from the name, actors or countries
def search(request):
    return render(request, 'search.html')
