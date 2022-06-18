from django.http import Http404
from django.shortcuts import render
import requests
from .forms import myRentalForms, mySignUpForms, myLogInForms
import math

username = ""

# Home Page
def home_page(request):
    tparams = {'username': username}
    return render(request, 'home_page.html', tparams)

# Sign Up
def signup(request):
    tparams = {'username': username}
    return render(request, 'signup.html', tparams)

# Sign Up Confirm
def signup_confirm(request):
    form = mySignUpForms(request.POST)
    data = {}
    if form.is_valid():
        data = form.cleaned_data
    response = requests.post(
        f"http://idp.moviefans.k3s/deti-egs-moviefan/Authentication/1.0.0/v1/signup",
        json=dict(username=data["username"], email=data["email"], password=data["password"])
    )
    global username
    username = data["username"]
    if (response.status_code != 200) or ("OK" not in response.text):
        username = ""
    tparams = {
        'username': username,
        'status' : response.json()["status"]
    }
    return render(request, 'signup_confirm.html', tparams)

# Login
def login(request):
    tparams = {'username': username}
    return render(request, 'login.html', tparams)

# Login Confirm
def login_confirm(request):
    form = myLogInForms(request.POST)
    data = {}
    if form.is_valid():
        data = form.cleaned_data
    response = requests.post(
        f"http://idp.moviefans.k3s/deti-egs-moviefan/Authentication/1.0.0/v1/auth-token",
        json=dict(username=data["username"], password=data["password"])
    )
    global username
    username = data["username"]
    if (response.status_code != 200) or ("OK" not in response.text):
        username = ""
    tparams = {
        'username': username,
        'status' : response.json()["status"]
    }
    return render(request, 'login_confirm.html', tparams)

# Log Out
def logout(request):
    global username
    bye_user = username
    username = ""
    tparams = {
        'username': username,
        'bye_user' : bye_user
    }
    return render(request, 'logout.html', tparams)

# Profile
def profile(request):
    user_rentals = requests.get("http://rental.k3s/rentals/rental/v1/productsBy/"+username).json()
    tparams = {
        'username': username,
        'user_rentals': user_rentals
    }
    return render(request, 'profile.html', tparams)

# List of all the movies
def movieslist(request):
    allmovies_ditc = requests.get("http://moviestats.k3s/v1/shows?type=movie").json()
    tparams = {
        'allmovies_ditc': allmovies_ditc,
        'username': username
    }
    return render(request, 'list_of_movies.html', tparams)

# Information about the movie/serie
def movie(request):
    if not 'id' in request.GET:
        raise Http404("Filme não disponível!")
    id = request.GET['id']
    movie_ditc = requests.get("http://moviestats.k3s/v1/movie/?show_id="+id).json()
    cast = movie_ditc["cast"].split(", ")
    cast_last_element = cast[-1]
    directors = movie_ditc["director"].split(", ")
    directors_last_element = directors[-1]
    countries = movie_ditc["country"].split(", ")
    countries_last_element = countries[-1]
    categories = movie_ditc["listed_in"].split(", ")
    categories_last_element = categories[-1]
    tparams = {
        'username': username,
        'movie': movie_ditc,
        'cast' : cast,
        'cast_last_element': cast_last_element,
        'directors' : directors,
        'directors_last_element': directors_last_element,
        'countries' : countries,
        'countries_last_element': countries_last_element,
        'categories' : categories,
        'categories_last_element': categories_last_element
    }
    return render(request, 'program_info.html', tparams)

# List of all the series
def serieslist(request):
    allseries_ditc = requests.get("http://moviestats.k3s/v1/shows?type=tvshow").json()
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
    movie_statistics = requests.get("http://moviestats.k3s/v1/movie/?show_id="+id).json()
    tparams = {
        'movie_statistics': movie_statistics,
        'username': username
    }
    return render(request, 'rent.html', tparams)

# Confirm Rent Movie
def rent_confirm(request): 
    if not 'id' in request.GET:
        raise Http404("Movie not available!")
    id = request.GET['id']
    form = myRentalForms(request.POST)
    data = {}
    if form.is_valid():
        data = form.cleaned_data
    error = False
    movie_data = {}
    if int(data["rental_time"]) > 100 or int(data["rental_time"]) < 1:
        error = True
    if not error:
        movie_title = requests.get("http://moviestats.k3s/v1/movie/?show_id="+id).json()["title"]
        movie_price = round(math.log(int(data["rental_time"])+1),2)*2
        movie_data = {"price": movie_price, "entity": "movie_fan", "username": username, "title": movie_title, "rental_time": data["rental_time"]}
        requests.post("http://rental.k3s/rentals/rental/v1/products/"+id, data = movie_data)
    tparams = {
        'movie_data' : movie_data,
        'username': username,
        'error' : error
    }
    return render(request, 'rent_confirm.html', tparams)

# Lists all movies/series of an actor
def actor(request):
    if not 'id' in request.GET:
        raise Http404("Actor não disponível!")
    id = request.GET['id']
    actor_ditc = requests.get("http://moviestats.k3s/v1/actor/?name="+id).json()
    tparams = {
        'username': username,
        'actor_ditc': actor_ditc,
        'actor_name': id,
        'number_of_shows': len(actor_ditc)
    }
    return render(request, 'actor.html', tparams)

# Lists all movies/series of a director
def director(request):
    if not 'id' in request.GET:
        raise Http404("Director não disponível!")
    id = request.GET['id']
    director_ditc = requests.get("http://moviestats.k3s/v1/director/?name="+id).json()
    tparams = {
        'username': username,
        'director_ditc': director_ditc,
        'director_name': id,
        'number_of_shows': len(director_ditc)
    }
    return render(request, 'director.html', tparams)

# Lists all movies/series directed in a country
def country(request):
    if not 'id' in request.GET:
        raise Http404("Country not available!")
    id = request.GET['id']
    country_ditc = requests.get("http://moviestats.k3s/v1/country/?name="+id).json()
    tparams = {
        'username': username,
        'country_ditc': country_ditc,
        'country_name': id,
        'number_of_shows': len(country_ditc)
    }
    return render(request, 'country.html', tparams)

# Lists all movies/series from a category (action, drama, comedy, etc.)
def category(request):
    if not 'id' in request.GET:
        raise Http404("Category not available!")
    id = request.GET['id']
    category_ditc = requests.get("http://moviestats.k3s/v1/listed_in/?name="+id).json()
    tparams = {
        'username': username,
        'category_ditc': category_ditc,
        'category_name': id,
        'number_of_shows': len(category_ditc)
    }
    return render(request, 'category.html', tparams)
