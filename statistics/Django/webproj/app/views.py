from django.shortcuts import render
from django.http import Http404, HttpResponse
from datetime import datetime
import json as simplejson 
import mariadb
import sys

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="root",
        password="root",
        host="127.0.0.1",
        port=3306,
        database="movies"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

def home(request):
    tparams = {
        'title': 'Home Page',
        'year': datetime.now().year,
    }
    return render(request, 'index.html', tparams)

def nmovies(request):
    tparams = {
        'title': 'Contact',
        'message': 'Your contact page.',
        'year': datetime.now().year,
    }
    return render(request, 'index.html', tparams)

def movie(request):
    if not 'show_id' in request.GET:
        raise Http404("Filme não disponível!")
    id = request.GET['show_id']
    print(id)
    cur = conn.cursor()
    data = (id, )
    statement ="select * from show_info where id=%d;"
    cur.execute(statement,data)
    myresult = cur.fetchall()
    cur.close()
    tparams = {
        'title': myresult[0],
    }
    return render(request, 'index.html', tparams)

def id(request):
    if not 'show_id' in request.GET:
        raise Http404("Filme não disponível!")
    id = request.GET['show_id']
    print(id)
    cur = conn.cursor()
    data = (id, )
    statement ="select id from show_info where id=%d;"
    cur.execute(statement,data)
    myresult = cur.fetchall()
    cur.close()
    tparams = {
        'title': myresult[0][0],
    }
    data = simplejson.dumps(tparams)
    return HttpResponse(data, content_type='application/json')

def type(request):
    if not 'show_id' in request.GET:
        raise Http404("Filme não disponível!")
    id = request.GET['show_id']
    print(id)
    cur = conn.cursor()
    data = (id, )
    statement ="select type from show_info where id=%d;"
    cur.execute(statement,data)
    myresult = cur.fetchall()
    cur.close()
    tparams = {
        'title': myresult[0][0],
    }
    data = simplejson.dumps(tparams)
    return HttpResponse(data, content_type='application/json')

def title(request):
    if not 'show_id' in request.GET:
        raise Http404("Filme não disponível!")
    id = request.GET['show_id']
    print(id)
    cur = conn.cursor()
    data = (id, )
    statement ="select title from show_info where id=%d;"
    cur.execute(statement,data)
    myresult = cur.fetchall()
    cur.close()
    tparams = {
        'title': myresult[0][0],
    }
    data = simplejson.dumps(tparams)
    return HttpResponse(data, content_type='application/json')

def director(request):
    if not 'show_id' in request.GET:
        raise Http404("Filme não disponível!")
    id = request.GET['show_id']
    print(id)
    cur = conn.cursor()
    data = (id, )
    statement ="select director from show_info where id=%d;"
    cur.execute(statement,data)
    myresult = cur.fetchall()
    cur.close()
    tparams = {
        'title': myresult[0][0],
    }
    data = simplejson.dumps(tparams)
    return HttpResponse(data, content_type='application/json')

def cast(request):
    if not 'show_id' in request.GET:
        raise Http404("Filme não disponível!")
    id = request.GET['show_id']
    print(id)
    cur = conn.cursor()
    data = (id, )
    statement ="select cast from show_info where id=%d;"
    cur.execute(statement,data)
    myresult = cur.fetchall()
    cur.close()
    tparams = {
        'title': myresult[0][0],
    }
    data = simplejson.dumps(tparams)
    return HttpResponse(data, content_type='application/json')

def country(request):
    if not 'show_id' in request.GET:
        raise Http404("Filme não disponível!")
    id = request.GET['show_id']
    print(id)
    cur = conn.cursor()
    data = (id, )
    statement ="select country from show_info where id=%d;"
    cur.execute(statement,data)
    myresult = cur.fetchall()
    cur.close()
    tparams = {
        'title': myresult[0][0],
    }
    data = simplejson.dumps(tparams)
    return HttpResponse(data, content_type='application/json')

def date_added(request):
    if not 'show_id' in request.GET:
        raise Http404("Filme não disponível!")
    id = request.GET['show_id']
    print(id)
    cur = conn.cursor()
    data = (id, )
    statement ="select date_added from show_info where id=%d;"
    cur.execute(statement,data)
    myresult = cur.fetchall()
    cur.close()
    tparams = {
        'title': myresult[0][0],
    }
    data = simplejson.dumps(tparams)
    return HttpResponse(data, content_type='application/json')

def release_year(request):
    if not 'show_id' in request.GET:
        raise Http404("Filme não disponível!")
    id = request.GET['show_id']
    print(id)
    cur = conn.cursor()
    data = (id, )
    statement ="select release_year from show_info where id=%d;"
    cur.execute(statement,data)
    myresult = cur.fetchall()
    cur.close()
    tparams = {
        'title': myresult[0][0],
    }
    data = simplejson.dumps(tparams)
    return HttpResponse(data, content_type='application/json')

def rating(request):
    if not 'show_id' in request.GET:
        raise Http404("Filme não disponível!")
    id = request.GET['show_id']
    print(id)
    cur = conn.cursor()
    data = (id, )
    statement ="select rating from show_info where id=%d;"
    cur.execute(statement,data)
    myresult = cur.fetchall()
    cur.close()
    tparams = {
        'title': myresult[0][0],
    }
    data = simplejson.dumps(tparams)
    return HttpResponse(data, content_type='application/json')

def duration(request):
    if not 'show_id' in request.GET:
        raise Http404("Filme não disponível!")
    id = request.GET['show_id']
    print(id)
    cur = conn.cursor()
    data = (id, )
    statement ="select duration from show_info where id=%d;"
    cur.execute(statement,data)
    myresult = cur.fetchall()
    cur.close()
    tparams = {
        'title': myresult[0][0],
    }
    data = simplejson.dumps(tparams)
    return HttpResponse(data, content_type='application/json')

def listed_in(request):
    if not 'show_id' in request.GET:
        raise Http404("Filme não disponível!")
    id = request.GET['show_id']
    print(id)
    cur = conn.cursor()
    data = (id, )
    statement ="select listed_in from show_info where id=%d;"
    cur.execute(statement,data)
    myresult = cur.fetchall()
    cur.close()
    tparams = {
        'title': myresult[0][0],
    }
    data = simplejson.dumps(tparams)
    return HttpResponse(data, content_type='application/json')

def description(request):
    if not 'show_id' in request.GET:
        raise Http404("Filme não disponível!")
    id = request.GET['show_id']
    print(id)
    cur = conn.cursor()
    data = (id, )
    statement ="select description from show_info where id=%d;"
    cur.execute(statement,data)
    myresult = cur.fetchall()
    cur.close()
    tparams = {
        'title': myresult[0][0],
    }
    data = simplejson.dumps(tparams)
    return HttpResponse(data, content_type='application/json')