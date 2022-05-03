from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
import json
from datetime import date
import requests
from django.shortcuts import render
from .forms import myRentalForms, mySignUpForms
import numpy as np

_endpoint = "http://localhost:7200"
_repositorio = "moviesDB"
client = ApiClient(endpoint=_endpoint)
accessor = GraphDBApi(client)
username = ""

# Home Page
def home_page(request):
    return render(request, 'home_page.html')

# Login
def login(request):
    return render(request, 'login.html')

# Sign Up
def signup(request):
    return render(request, 'signup.html')

# Sign Up Confirm
def profile(request):
    form = mySignUpForms(request.POST)
    data = {}
    if form.is_valid():
        data = form.cleaned_data

    global username
    username = data["username"]
    print(username)

    print("username: ", data["username"])
    print("password: ", data["password"])
    print("email: ", data["email"])

    response = requests.post(
        f"http://localhost:8001/deti-egs-moviefan/Authentication/1.0.0/v1/signup",
        json=dict(username=data["username"], email=data["email"], password=data["password"])
    )
    print('Response body is : ' + response.text)

    error = False
    if (response.status_code != 200):
        error = True
    if "OK" not in response.text:
        error = True

    tparams = {
        'username': data["username"],
        'error' : error,
        'response' : response.text
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

# All information about a movie/show from its id
def getShowInfo(id):
    aux = id
    id='<http://movies.org/title/'+id+'>'
    query = "PREFIX mov: <http://movies.org/pred/>" \
            "select ?name ?typename ?date ?year ?rating ?duration ?listed ?des ?rate ?quality ?watched " \
            "where {" \
            "    " + id + " mov:name ?name ." \
            "    " + id + " mov:type ?type ." \
            "    ?type  mov:name ?typename ." \
            "    " + id + " mov:date_added ?date ." \
            "    " + id + " mov:release_year ?year ." \
            "    " + id + " mov:rating ?rating ." \
            "    " + id + " mov:duration ?duration ." \
            "    " + id + " mov:listed_in ?listed ." \
            "    " + id + " mov:description ?des ." \
            "OPTIONAL{" + id + " mov:rate ?rate . }" \
            "OPTIONAL{" + id + " mov:quality ?quality . }" \
            "OPTIONAL{" + id + " mov:watched ?watched . }" \
            "}"

    _body = {"query": query}
    res = accessor.sparql_select(body=_body, repo_name=_repositorio)
    res = json.loads(res)

    info = dict()
    info["full_id"] = 'http://movies.org/title/' + aux
    info["id"] = aux
    for key in res['results']['bindings']:
        info['name'] = key['name']['value']
        info['type'] = key['typename']['value']
        info['release_year'] = key['year']['value']
        info['rating'] = key['rating']['value']
        info['duration'] = key['duration']['value']
        info['listed_in'] = key['listed']['value']
        info['description'] = key['des']['value']
        info['date_added'] = key['date']['value']
        if 'rate' in key and 'quality' in key:
            info['rate'] = key['rate']['value']
            info['quality'] = key['quality']['value']
        if 'watched' in key:
            info['watched'] = key['watched']['value']

    # Directors
    query = "PREFIX mov: <http://movies.org/pred/>" \
            "select ?dirname " \
            "where {" \
            "    " + id + " mov:directed_by ?director ." \
            "    ?director  mov:name ?dirname ." \
            "}"

    _body = {"query": query}
    res = accessor.sparql_select(body=_body, repo_name=_repositorio)
    res = json.loads(res)
    directors = []

    for key in res['results']['bindings']:
        directors.append(key['dirname']['value'])

    info['director'] = directors

    # Actors
    query = "PREFIX mov: <http://movies.org/pred/>" \
            "select ?actorname " \
            "where {" \
            "    " + id + " mov:starring ?actor ." \
            "    ?actor  mov:name ?actorname ." \
            "}" \

    _body = {"query": query}
    res = accessor.sparql_select(body=_body, repo_name=_repositorio)
    res = json.loads(res)
    actor = []

    for key in res['results']['bindings']:
        actor.append(key['actorname']['value'])

    info['cast'] = actor

    # Countries
    query = "PREFIX mov: <http://movies.org/pred/>" \
            "select ?countryname " \
            "where {" \
            "    " + id + " mov:country ?country ." \
            "    ?country  mov:name ?countryname ." \
            "}"
    _body = {"query": query}
    res = accessor.sparql_select(body=_body, repo_name=_repositorio)
    res = json.loads(res)
    country = []

    for key in res['results']['bindings']:
        country.append(key['countryname']['value'])

    info['country'] = country

    # Categories
    query = "PREFIX mov: <http://movies.org/pred/>" \
            "select ?category_name " \
            "where {" \
            "    " + id + " mov:listed_in ?category ." \
            "    ?category  mov:name ?category_name ." \
            "}"
    _body = {"query": query}
    res = accessor.sparql_select(body=_body, repo_name=_repositorio)
    res = json.loads(res)
    category = []

    for key in res['results']['bindings']:
        category.append(key['category_name']['value'])

    info['category'] = category

    return info

# Lists all movies/series of an actor
def actor(request):
    # if not 'actor' in request.GET:
    #     raise Http404("Ator não disponível!")
    # ator = request.GET['actor']
    # info = getActorInfo(ator)

    # tparams = {
    #     'actor': info,
    # }

    return render(request, 'actor.html')

# Gets all the actor information
def getActorInfo(ator):
    query = "PREFIX mov: <http://movies.org/pred/>" \
            "SELECT distinct ?s ?movie ?a " \
            "WHERE" \
            "{" \
            "?a mov:name '" + ator + "' ."\
            "?s mov:starring ?a ." \
            "?s mov:name ?movie ." \
            "}" \

    _body = {"query": query}
    res = accessor.sparql_select(body=_body, repo_name=_repositorio)
    res = json.loads(res)

    list_movies = []
    ls_uri = []
    actor_uri = ""

    for key in res['results']['bindings']:
        list_movies.append(key['movie']['value'])
        str = key['s']['value'].split('/')
        ls_uri.append(str[4])

    query = "PREFIX mov: <http://movies.org/pred/>" \
            "SELECT distinct ?a " \
            "WHERE" \
            "{" \
            "?a mov:name '" + ator + "' ." \
            "}"

    _body = {"query": query}
    res = accessor.sparql_select(body=_body, repo_name=_repositorio)
    res = json.loads(res)

    for key in res['results']['bindings']:
        actor_uri = key['a']['value']

    info = dict()
    info['movies'] = {ls_uri.strip(): list_movies.strip() for ls_uri, list_movies in zip(ls_uri, list_movies)}
    info['number'] = len(list_movies)
    info['name'] = ator
    info['uri'] = actor_uri

    return info

# Lists all movies/series of a director
def director(request):
    # if not 'director' in request.GET:
    #     raise Http404("Diretor não disponível!")
    # diretor = request.GET['director']
    # info = getDirectorInfo(diretor)

    # tparams = {
    #     'director': info,
    # }

    return render(request, 'director.html')

# Gets all the director information
def getDirectorInfo(diretor):
    query = "PREFIX mov: <http://movies.org/pred/>" \
            "SELECT distinct ?s ?movie " \
            "WHERE" \
            "{" \
            "?a mov:name '" + diretor + "' ."\
            "?s mov:directed_by ?a ." \
            "?s mov:name ?movie ." \
            "}" \

    _body = {"query": query}
    res = accessor.sparql_select(body=_body, repo_name=_repositorio)
    res = json.loads(res)

    list_movies = []
    ls_uri = []
    director_uri = ""

    for key in res['results']['bindings']:
        list_movies.append(key['movie']['value'])
        str = key['s']['value'].split('/')
        ls_uri.append(str[4])

    query = "PREFIX mov: <http://movies.org/pred/>" \
            "SELECT distinct ?a " \
            "WHERE" \
            "{" \
            "?a mov:name '" + diretor + "' ." \
            "}" \

    _body = {"query": query}
    res = accessor.sparql_select(body=_body, repo_name=_repositorio)
    res = json.loads(res)

    for key in res['results']['bindings']:
        director_uri = key['a']['value']

    info = dict()
    info['movies'] = {ls_uri.strip(): list_movies.strip() for ls_uri, list_movies in zip(ls_uri, list_movies)}
    info['number'] = len(list_movies)
    info['name'] = diretor
    info['uri'] = director_uri

    return info

# Lists all movies/series directed in a country
def country(request):
    # if not 'country' in request.GET:
    #     raise Http404("Country unavailable!")
    # c = request.GET['country']
    # info = getCountryInfo(c)

    # tparams = {
    #     'country': info,
    # }

    return render(request, 'country.html')

# Gets the country information
def getCountryInfo(c):
    query = "PREFIX mov: <http://movies.org/pred/>" \
            "SELECT distinct ?s ?movie " \
            "WHERE" \
            "{" \
            "?a mov:name '" + c + "' ."\
            "?s mov:country ?a ." \
            "?s mov:name ?movie ." \
            "}" \

    _body = {"query": query}
    res = accessor.sparql_select(body=_body, repo_name=_repositorio)
    res = json.loads(res)

    list_movies = []
    ls_uri = []
    country_uri = ""

    for key in res['results']['bindings']:
        list_movies.append(key['movie']['value'])
        str = key['s']['value'].split('/')
        ls_uri.append(str[4])

    query = "PREFIX mov: <http://movies.org/pred/>" \
            "SELECT distinct ?a " \
            "WHERE" \
            "{" \
            "?a mov:name '" + c + "' ." \
            "}" \

    _body = {"query": query}
    res = accessor.sparql_select(body=_body, repo_name=_repositorio)
    res = json.loads(res)

    for key in res['results']['bindings']:
        country_uri = key['a']['value']


    info = dict()
    info['movies'] = {ls_uri.strip(): list_movies.strip() for ls_uri, list_movies in zip(ls_uri, list_movies)}
    info['number'] = len(list_movies)
    info['name'] = c
    info['uri'] = country_uri

    return info

# Lists all movies/series from a category (action, drama, comedy, etc.)
def category(request):
    # if not 'category' in request.GET:
    #     raise Http404("Category unavailable!")
    # cat = request.GET['category']
    # info = getCategoryInfo(cat)

    # tparams = {
    #     'category': info,
    # }

    return render(request, 'category.html')

# Gets the category information
def getCategoryInfo(cat):
    query = "PREFIX mov: <http://movies.org/pred/>" \
            "SELECT distinct ?s ?movie " \
            "WHERE" \
            "{" \
            "?a mov:name '" + cat + "' ."\
            "?s mov:listed_in ?a ." \
            "?s mov:name ?movie ." \
            "}" \

    _body = {"query": query}
    res = accessor.sparql_select(body=_body, repo_name=_repositorio)
    res = json.loads(res)

    list_movies = []
    ls_uri = []
    category_uri = ""

    for key in res['results']['bindings']:
        list_movies.append(key['movie']['value'])
        str = key['s']['value'].split('/')
        ls_uri.append(str[4])

    query = "PREFIX mov: <http://movies.org/pred/>" \
            "SELECT distinct ?a " \
            "WHERE" \
            "{" \
            "?a mov:name '" + cat + "' ." \
            "}"

    _body = {"query": query}
    res = accessor.sparql_select(body=_body, repo_name=_repositorio)
    res = json.loads(res)

    for key in res['results']['bindings']:
        category_uri = key['a']['value']

    info = dict()
    info['movies'] = {ls_uri.strip(): list_movies.strip() for ls_uri, list_movies in zip(ls_uri, list_movies)}
    info['number'] = len(list_movies)
    info['name'] = cat
    info['uri'] = category_uri

    return info

# Searches for movies from the name, actors or countries
def search(request):
    # assert isinstance(request, HttpRequest)
    # if 'serieName' in request.POST:
    #     countryName = request.POST['countryName']
    #     serieName = request.POST['serieName']
    #     actorName = request.POST['actorName']

    #     if serieName:
    #         query = "PREFIX mov: <http://movies.org/pred/>" \
    #                 "select ?s ?movie " \
    #                 "where {" \
    #                 "    ?s mov:type ?a ." \
    #                 "    ?s mov:name ?movie ." \
    #                 "FILTER regex(?movie, '" + serieName + "', 'i')" \
    #         "}"

    #         _body = {"query": query}
    #         res = accessor.sparql_select(body=_body, repo_name=_repositorio)
    #         res = json.loads(res)
    #         ls = []
    #         ls_uri = []
    #         for key in res['results']['bindings']:
    #             ls.append(key['movie']['value'])
    #             str = key['s']['value'].split('/')
    #             ls_uri.append(str[4])

    #         info = {ls_uri.strip(): ls.strip() for ls_uri, ls in zip(ls_uri, ls)}

    #         tparams = {
    #             'search': info,
    #         }
    #         return render(request, 'list_of_movies.html', tparams)

    #     elif countryName:
    #         query = "PREFIX mov: <http://movies.org/pred/>" \
    #                 "select ?s ?movie " \
    #                 "where {" \
    #                 "    ?country mov:name ?cName ." \
    #                 "    ?s mov:country ?country ." \
    #                 "    ?s mov:name ?movie" \
    #                 "   FILTER regex(?cName, '" + countryName + "', 'i')" \
    #                 "}"

    #         _body = {"query": query}
    #         res = accessor.sparql_select(body=_body, repo_name=_repositorio)
    #         res = json.loads(res)
    #         ls = []
    #         ls_uri = []

    #         for key in res['results']['bindings']:
    #             ls.append(key['movie']['value'])
    #             str = key['s']['value'].split('/')
    #             ls_uri.append(str[4])

    #         info = {ls_uri.strip(): ls.strip() for ls_uri, ls in zip(ls_uri, ls)}

    #         tparams = {
    #             'search': info,
    #         }
    #         return render(request, 'list_of_movies.html', tparams)

    #     elif actorName:
    #         query = "PREFIX mov: <http://movies.org/pred/>" \
    #                 "select ?s ?movie " \
    #                 "where {" \
    #                 "    ?actor mov:name ?cName ." \
    #                 "    ?s mov:starring ?actor ." \
    #                 "    ?s mov:name ?movie" \
    #                 "   FILTER regex(?cName, '" + actorName + "', 'i')" \
    #                                                             "}"

    #         _body = {"query": query}
    #         res = accessor.sparql_select(body=_body, repo_name=_repositorio)
    #         res = json.loads(res)
    #         ls = []
    #         ls_uri = []

    #         for key in res['results']['bindings']:
    #             ls.append(key['movie']['value'])
    #             str = key['s']['value'].split('/')
    #             ls_uri.append(str[4])

    #         info = {ls_uri.strip(): ls.strip() for ls_uri, ls in zip(ls_uri, ls)}

    #         tparams = {
    #             'search': info,
    #         }
    #         return render(request, 'list_of_movies.html', tparams)
    #     else:
    #         return render(request, 'list_of_movies.html', {'Error': True, })
    # else:
    #     query = '''PREFIX mov: <http://movies.org/pred/>
    #                 SELECT distinct ?name
    #                 WHERE
    #                 {
    #                   ?s mov:listed_in ?o .
    #                   ?o mov:name ?name .
    #                 }
    #                 GROUP BY ?name
    #                 Order by desc(COUNT(?o))'''

    #     _body = {"query": query}
    #     res = accessor.sparql_select(body=_body, repo_name=_repositorio)
    #     res = json.loads(res)
    #     ls = []
    #     for key in res['results']['bindings']:
    #         ls.append(key['name']['value'])


    #     tparams = {
    #         'search': ls
    #     }
        return render(request, 'search.html')

# Lists the actors with more than 10 movies
# Inference by rule (more than 10 movies) = popular
def popular_actors(request):
    # query = '''
    #         PREFIX mov: <http://movies.org/pred/>
    #         SELECT distinct ?name (COUNT(?s) as ?pCount)
    #         WHERE {
    #             ?s mov:starring ?id .
    #             ?id mov:name ?name .
    #             ?s mov:name ?movie .
    #         }
    #         GROUP BY ?name
    #         HAVING(?pCount>10)
    #         ORDER BY desc(?pCount)
    #         '''

    # _body = {"query": query}
    # res = accessor.sparql_select(body=_body, repo_name=_repositorio)
    # res = json.loads(res)
    # ls_popular = []

    # for key in res['results']['bindings']:
    #     ls_popular.append(key['name']['value'])

    # ls_all = rest_of_actors()

    # tparams = {
    #     'search': ls_popular,
    #     'all': ls_all
    # }

    return render(request, 'popular_actors.html')

# Lists all the other actors (<11 movies)
def rest_of_actors():
    query = '''
            PREFIX mov: <http://movies.org/pred/>
            SELECT distinct ?name (COUNT(?s) as ?pCount)
            WHERE {
                ?s mov:starring ?id .
                ?id mov:name ?name .
                ?s mov:name ?movie .
            }
            GROUP BY ?name
            HAVING(?pCount<11)
            ORDER BY desc(?pCount)
            '''

    _body = {"query": query}
    res = accessor.sparql_select(body=_body, repo_name=_repositorio)
    res = json.loads(res)
    ls_all = []

    for key in res['results']['bindings']:
        ls_all.append(key['name']['value'])

    return ls_all

# Lists the directors with more than 10 movies
# Inference by rule (more than 10 movies) = popular
def popular_directors(request):
    # query = '''
    #         PREFIX mov: <http://movies.org/pred/>
    #         SELECT distinct ?name (COUNT(?s) as ?pCount)
    #         WHERE {
    #             ?s mov:directed_by ?id .
    #             ?id mov:name ?name .
    #             ?s mov:name ?movie .
    #         }
    #         GROUP BY ?name
    #         HAVING(?pCount>10)
    #         ORDER BY desc(?pCount)
    #         '''

    # _body = {"query": query}
    # res = accessor.sparql_select(body=_body, repo_name=_repositorio)
    # res = json.loads(res)
    # ls_popular = []

    # for key in res['results']['bindings']:
    #     ls_popular.append(key['name']['value'])

    # ls_all = rest_of_directors()

    # tparams = {
    #     'search': ls_popular,
    #     'all': ls_all
    # }
    return render(request, 'popular_directors.html')

# Lists all the other directors (<11 movies)
def rest_of_directors():
    query = '''
            PREFIX mov: <http://movies.org/pred/>
            SELECT distinct ?name (COUNT(?s) as ?pCount)
            WHERE {
                ?s mov:directed_by ?id .
                ?id mov:name ?name .
                ?s mov:name ?movie .
            }
            GROUP BY ?name
            HAVING(?pCount<11)
            ORDER BY desc(?pCount)
            '''

    _body = {"query": query}
    res = accessor.sparql_select(body=_body, repo_name=_repositorio)
    res = json.loads(res)
    ls_all = []

    for key in res['results']['bindings']:
        ls_all.append(key['name']['value'])

    return ls_all

# Rating of the movies/series
def add_rating_1(request):
    # id = request.GET['id']
    # tparams = add_rating(id, '1')
    return render(request, 'program_info.html')

def add_rating_2(request):
    # id = request.GET['id']
    # tparams = add_rating(id, '2')
    return render(request, 'program_info.html')

def add_rating_3(request):
    # id = request.GET['id']
    # tparams = add_rating(id, '3')
    return render(request, 'program_info.html')

def add_rating_4(request):
    # id = request.GET['id']
    # tparams = add_rating(id, '4')
    return render(request, 'program_info.html')

def add_rating_5(request):
    # id = request.GET['id']
    # tparams = add_rating(id, '5')
    return render(request, 'program_info.html')

# Rent Movie
def rent(request):
    if not 'id' in request.GET:
        raise Http404("Filme não disponível!")
    id = request.GET['id']
    movie_statistics = requests.get("http://127.0.0.1:8003/v1/movie/?show_id="+id).json()
    
    print(username)
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
    print(data)
    print(username)

    movie_title = requests.get("http://127.0.0.1:8003/v1/movie/?show_id="+id).json()["title"]
    movie_price = round(np.log(int(data["rental_time"])+1),2)*2
    movie_data = {"price": movie_price, "entity": "movie_fan", "username": username, "title": movie_title, "rental_time": data["rental_time"]}

    requests.post("http://127.0.0.1:8002/rentals/rental/v1/products/"+id, data = movie_data)

    tparams = {
        'movie_data' : movie_data
    }

    return render(request, 'rent_confirm.html', tparams)

# Marks the movie as unwatched
def mark_unwatched(request):
    # id = request.GET['id']
    # tparams = mark_as_unwatched(id)
    return render(request, 'program_info.html')

# Adds the rating to the database
def add_rating(id, rating):
    info = getShowInfo(id)

    update = "PREFIX pred: <http://movies.org/pred/>" \
            "PREFIX subj: <http://movies.org/title/>" \
            "DELETE WHERE {subj:" + id + " pred:rate ?o}"

    _body = {"update": update}
    res = accessor.sparql_update(body=_body,repo_name=_repositorio)

    update = "PREFIX pred: <http://movies.org/pred/>" \
            "PREFIX subj: <http://movies.org/title/>" \
            "DELETE WHERE {subj:" + id + " pred:quality ?o}"

    _body = {"update": update}
    res = accessor.sparql_update(body=_body,repo_name=_repositorio)


    update = "PREFIX pred: <http://movies.org/pred/>" \
            "PREFIX subj: <http://movies.org/title/>" \
            "INSERT DATA {subj:" + id + " pred:rate '" + rating + "'}"

    _body = {"update": update}
    res = accessor.sparql_update(body=_body,repo_name=_repositorio)
    rating = int(rating)

    # Inference by judgement
    if rating > 3 and info['type'] == 'TV Show':
        quality = 'Good Show!'
    elif rating > 3 and info['type'] == 'Movie':
        quality = 'Good Movie!'
    elif rating < 3 and info['type'] == 'TV Show':
        quality = 'Bad Show!'
    elif rating < 3 and info['type'] == 'Movie':
        quality = 'Bad Movie!'
    elif rating == 3 and info['type'] == 'TV Show':
        quality = 'Average Show!'
    else:
        quality = 'Average Movie!'

    update2 = "PREFIX pred: <http://movies.org/pred/>" \
             "PREFIX subj: <http://movies.org/title/>" \
             "INSERT DATA {subj:" + id + " pred:quality '" + quality + "'}"

    _body2 = {"update": update2}
    res = accessor.sparql_update(body=_body2, repo_name=_repositorio)

    info = getShowInfo(id)
    tparams = {
        'movie': info,
    }
    return tparams

# Adds the 'watched' to the database
def mark_as_watched(id):
    update = "PREFIX pred: <http://movies.org/pred/>" \
            "PREFIX subj: <http://movies.org/title/>" \
            "INSERT DATA {subj:" + id + " pred:watched 'True'}"

    _body = {"update": update}
    res = accessor.sparql_update(body=_body,repo_name=_repositorio)

    info = getShowInfo(id)
    tparams = {
        'movie': info,
    }
    return tparams

# Deletes the 'watched' from the database
def mark_as_unwatched(id):
    update = "PREFIX pred: <http://movies.org/pred/>" \
            "PREFIX subj: <http://movies.org/title/>" \
            "DELETE WHERE {subj:" + id + " pred:watched 'True'}"

    _body = {"update": update}
    res = accessor.sparql_update(body=_body,repo_name=_repositorio)

    info = getShowInfo(id)
    tparams = {
        'movie': info,
    }
    return tparams
