from django.shortcuts import render
from django.http import Http404, HttpResponse
from datetime import datetime
import json as simplejson 
import pymongo
import csv

# Connect to MongoDB Platform
client = pymongo.MongoClient("mongo", 27017)
db = client.movies

with open('app/movies.csv', 'r') as f:

    csvreader = csv.reader(f)
    header = next(csvreader)
    i = 0

    results = db.show_info.find()
    count=0
    for i in results:
        count+=1
        if count>2:
            break
    
    if count==0:
        for row in csvreader:
            try:

                dict = {'id': i,
                        'type': row[1],
                        'title': row[2],
                        'director': row[3],
                        'cast': row[4],
                        'country': row[5],
                        'date_added': row[6],
                        'release_year': row[7],
                        'rating': row[8],
                        'duration': row[9],
                        'listed_in': row[10],
                        'description': row[11]
                        }
                dict1 = {
                    'id':i,
                    'nranks':0,
                    'sumranks':0
                }
                i += 1
                if i % 100 == 0:
                    print(i)

                db.show_info.insert_one(dict)
                db.show_rank.insert_one(dict1)
            except:
                pass



def home(request):
    tparams = {
        'title': 'Home Page',
        'year': datetime.now().year,
    }
    return render(request, 'index.html', tparams)

def nmovies(request):
    print("OK1")
    db.show_info.insert_one({'movie':'terminator'})
    print("OK2")
    results = db.show_info.find()
    count=0
    for i in results:
        count+=1
    
    tparams = {
        'title': count
    }
    data = simplejson.dumps(tparams)
    return HttpResponse(data, content_type='application/json')
    
def shows(request):
    if not 'type' in request.GET:
        raise Http404("Invalid request!")
    type = request.GET['type']
    if type=='movie':
        statement = "{type = 'Movie'}"
    elif type=='tvshow':
        statement = "{type = 'tv show'}"
    else:
        tparams = {
        'title': 'error'
        }
        data = simplejson.dumps(tparams)
        return HttpResponse(data, content_type='application/json')
    results = db.show_info.find()
    tparams = {}
    for i in results:
        movie = {
        'id': i['id'],
        'type': i['type'],
        'title': i['title'],
        'director': i['director'],
        'cast': i['cast'],
        'country': i['country'],
        'date_added': i['date_added'],
        'release_year': i['release_year'],
        'rating': i['rating'],
        'duration': i['duration'],
        'listed_in': i['listed_in'],
        'description': i['description']
        }
        tparams[i['id']]=movie
    data = simplejson.dumps(tparams)
    return HttpResponse(data, content_type='application/json')

#partial search
def actor(request):
    if not 'name' in request.GET:
        raise Http404("Invalid request!")
    name = request.GET['name']
    # quote = "{'cast' : /aniston/}"
    # results = db.show_info.find(dict(quote))
    # print(quote)
    # print(results)
    results = db.show_info.find()
    tparams = {}
    for i in results:
        if name in i['cast'].casefold():
            movie = {
            'id': i['id'],
            'type': i['type'],
            'title': i['title'],
            'director': i['director'],
            'cast': i['cast'],
            'country': i['country'],
            'date_added': i['date_added'],
            'release_year': i['release_year'],
            'rating': i['rating'],
            'duration': i['duration'],
            'listed_in': i['listed_in'],
            'description': i['description']
            }
            tparams[i['id']]=movie
    data = simplejson.dumps(tparams)
    return HttpResponse(data, content_type='application/json')

#partial search
def director_list(request):
    if not 'name' in request.GET:
        raise Http404("Invalid request!")
    name = request.GET['name']
    results = db.show_info.find()
    tparams = {}
    for i in results:
        if name in i['director'].casefold():
            movie = {
            'id': i['id'],
            'type': i['type'],
            'title': i['title'],
            'director': i['director'],
            'cast': i['cast'],
            'country': i['country'],
            'date_added': i['date_added'],
            'release_year': i['release_year'],
            'rating': i['rating'],
            'duration': i['duration'],
            'listed_in': i['listed_in'],
            'description': i['description']
            }
            tparams[i['id']]=movie
    data = simplejson.dumps(tparams)
    return HttpResponse(data, content_type='application/json')

#partial search
def country_search(request):
    if not 'name' in request.GET:
        raise Http404("Invalid request!")
    name = request.GET['name']
    results = db.show_info.find()
    tparams = {}
    for i in results:
        if name in i['country'].casefold():
            movie = {
            'id': i['id'],
            'type': i['type'],
            'title': i['title'],
            'director': i['director'],
            'cast': i['cast'],
            'country': i['country'],
            'date_added': i['date_added'],
            'release_year': i['release_year'],
            'rating': i['rating'],
            'duration': i['duration'],
            'listed_in': i['listed_in'],
            'description': i['description']
            }
            tparams[i['id']]=movie
    data = simplejson.dumps(tparams)
    return HttpResponse(data, content_type='application/json')

#partial search
def listed_in_search(request):
    if not 'name' in request.GET:
        raise Http404("Invalid request!")
    name = request.GET['name']
    results = db.show_info.find()
    tparams = {}
    for i in results:
        if name in i['listed_in'].casefold():
            movie = {
            'id': i['id'],
            'type': i['type'],
            'title': i['title'],
            'director': i['director'],
            'cast': i['cast'],
            'country': i['country'],
            'date_added': i['date_added'],
            'release_year': i['release_year'],
            'rating': i['rating'],
            'duration': i['duration'],
            'listed_in': i['listed_in'],
            'description': i['description']
            }
            tparams[i['id']]=movie
    data = simplejson.dumps(tparams)
    return HttpResponse(data, content_type='application/json')

def movie(request):
    if not 'show_id' in request.GET:
        raise Http404("Filme não disponível!")
    id = request.GET['show_id']
    full_results = db.show_info.find({'id': int(id)})
    tparams={}
    for results in full_results:
        tparams = {
            'id': results['id'],
            'type': results['type'],
            'title': results['title'],
            'director': results['director'],
            'cast': results['cast'],
            'country': results['country'],
            'date_added': results['date_added'],
            'release_year': results['release_year'],
            'rating': results['rating'],
            'duration': results['duration'],
            'listed_in': results['listed_in'],
            'description': results['description']
        }

    data = simplejson.dumps(tparams)
    return HttpResponse(data, content_type='application/json')

def id(request):
    if not 'show_id' in request.GET:
        raise Http404("Filme não disponível!")
    id = request.GET['show_id']
    full_results = db.show_info.find({'id': int(id)})
    tparams={}
    for results in full_results:
        print("ENTRA")
        tparams = {
            'title': results['id'],
        }

    data = simplejson.dumps(tparams)
    return HttpResponse(data, content_type='application/json')

def type(request):
    if not 'show_id' in request.GET:
        raise Http404("Filme não disponível!")
    id = request.GET['show_id']
    full_results = db.show_info.find({'id': int(id)})
    tparams={}
    for results in full_results:
        tparams = {
            'title': results['type'],
        }

    data = simplejson.dumps(tparams)
    return HttpResponse(data, content_type='application/json')

def title(request):
    if not 'show_id' in request.GET:
        raise Http404("Filme não disponível!")
    id = request.GET['show_id']
    full_results = db.show_info.find({'id': int(id)})
    tparams={}
    for results in full_results:
        tparams = {
            'title': results['title'],
        }

    data = simplejson.dumps(tparams)
    return HttpResponse(data, content_type='application/json')

def director(request):
    if not 'show_id' in request.GET:
        raise Http404("Filme não disponível!")
    id = request.GET['show_id']
    full_results = db.show_info.find({'id': int(id)})
    tparams={}
    for results in full_results:
        tparams = {
            'title': results['director'],
        }

    data = simplejson.dumps(tparams)
    return HttpResponse(data, content_type='application/json')

def cast(request):
    if not 'show_id' in request.GET:
        raise Http404("Filme não disponível!")
    id = request.GET['show_id']
    full_results = db.show_info.find({'id': int(id)})
    tparams={}
    for results in full_results:
        tparams = {
            'title': results['cast'],
        }

    data = simplejson.dumps(tparams)
    return HttpResponse(data, content_type='application/json')

def country(request):
    if not 'show_id' in request.GET:
        raise Http404("Filme não disponível!")
    id = request.GET['show_id']
    full_results = db.show_info.find({'id': int(id)})
    tparams={}
    for results in full_results:
        tparams = {
            'title': results['country'],
        }

    data = simplejson.dumps(tparams)
    return HttpResponse(data, content_type='application/json')

def date_added(request):
    if not 'show_id' in request.GET:
        raise Http404("Filme não disponível!")
    id = request.GET['show_id']
    full_results = db.show_info.find({'id': int(id)})
    tparams={}
    for results in full_results:
        tparams = {
            'title': results['date_added'],
        }

    data = simplejson.dumps(tparams)
    return HttpResponse(data, content_type='application/json')

def release_year(request):
    if not 'show_id' in request.GET:
        raise Http404("Filme não disponível!")
    id = request.GET['show_id']
    full_results = db.show_info.find({'id': int(id)})
    tparams={}
    for results in full_results:
        tparams = {
            'title': results['release_year'],
        }

    data = simplejson.dumps(tparams)
    return HttpResponse(data, content_type='application/json')

def rating(request):
    if not 'show_id' in request.GET:
        raise Http404("Filme não disponível!")
    id = request.GET['show_id']
    full_results = db.show_info.find({'id': int(id)})
    tparams={}
    for results in full_results:
        tparams = {
            'title': results['rating'],
        }

    data = simplejson.dumps(tparams)
    return HttpResponse(data, content_type='application/json')

def duration(request):
    if not 'show_id' in request.GET:
        raise Http404("Filme não disponível!")
    id = request.GET['show_id']
    full_results = db.show_info.find({'id': int(id)})
    tparams={}
    for results in full_results:
        tparams = {
            'title': results['duration'],
        }

    data = simplejson.dumps(tparams)
    return HttpResponse(data, content_type='application/json')

def listed_in(request):
    if not 'show_id' in request.GET:
        raise Http404("Filme não disponível!")
    id = request.GET['show_id']
    full_results = db.show_info.find({'id': int(id)})
    tparams={}
    for results in full_results:
        tparams = {
            'title': results['listed_in'],
        }

    data = simplejson.dumps(tparams)
    return HttpResponse(data, content_type='application/json')

def description(request):
    if not 'show_id' in request.GET:
        raise Http404("Filme não disponível!")
    id = request.GET['show_id']
    full_results = db.show_info.find({'id': int(id)})
    tparams={}
    for results in full_results:
        tparams = {
            'title': results['description'],
        }

    data = simplejson.dumps(tparams)
    return HttpResponse(data, content_type='application/json')

def rank(request):
    if not 'rank' or not 'show_id' in request.POST:
        if not 'show_id' in request.GET:
            raise Http404("Filme não disponível!")
        id = request.GET['show_id']
        full_results = db.show_rank.find({'id': int(id)})
        tparams={}
        rank_sum=0
        n_evaluations=0
        for results in full_results:
            rank_sum = results['sumranks']
            n_evaluations = results['nranks']

        try:
            ranking=rank_sum/n_evaluations
        except:
            print("NO RANKING")
            ranking=0

        tparams = {
            'Our_rating': ranking,
            'n_evaluations': n_evaluations
        }
        data = simplejson.dumps(tparams)
        return HttpResponse(data, content_type='application/json')

    id = request.POST['show_id']
    rank = request.POST['rank']

    full_results = db.show_rank.find({'id': int(id)})

    for results in full_results:
            old_rank_sum = results['sumranks']
            old_n_evaluations = results['nranks']

    new_nranks=old_n_evaluations+1
    new_sumranks=old_rank_sum+int(rank)
    filter = {"id":int(id)}
    newvalues = { "$set": { 'nranks': new_nranks, 'sumranks':new_sumranks } }
    db.show_rank.update_one(filter,newvalues)

    tparams = {
        'rank': rank,
    }
    data = simplejson.dumps(tparams)
    return HttpResponse(data, content_type='application/json')
