from django.shortcuts import render
from datetime import datetime
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
    cur = conn.cursor()
    cur.execute("select * from show_info where id=1;")
    myresult = cur.fetchall()
    #print(myresult)
    cur.close()
    tparams = {
        'title': myresult[0],
        'message': 'Your contact page.',
        'year': datetime.now().year,
    }
    return render(request, 'index.html', tparams)

def id(request):
    cur = conn.cursor()
    cur.execute("select id from show_info where id=1;")
    myresult = cur.fetchall()
    #print(myresult)
    cur.close()
    tparams = {
        'title': myresult[0][0],
        'message': 'Your application description page.',
        'year': datetime.now().year,
    }
    return render(request, 'index.html', tparams)

def type(request):
    cur = conn.cursor()
    cur.execute("select type from show_info where id=1;")
    myresult = cur.fetchall()
    #print(myresult)
    cur.close()
    tparams = {
        'title': myresult[0][0],
        'message': 'Your application description page.',
        'year': datetime.now().year,
    }
    return render(request, 'index.html', tparams)

def title(request):
    cur = conn.cursor()
    cur.execute("select title from show_info where id=1;")
    myresult = cur.fetchall()
    #print(myresult)
    cur.close()
    tparams = {
        'title': myresult[0][0],
        'message': 'Your application description page.',
        'year': datetime.now().year,
    }
    return render(request, 'index.html', tparams)

def director(request):
    cur = conn.cursor()
    cur.execute("select director from show_info where id=1;")
    myresult = cur.fetchall()
    #print(myresult)
    cur.close()
    tparams = {
        'title': myresult[0][0],
        'message': 'Your application description page.',
        'year': datetime.now().year,
    }
    return render(request, 'index.html', tparams)

def cast(request):
    cur = conn.cursor()
    cur.execute("select cast from show_info where id=1;")
    myresult = cur.fetchall()
    #print(myresult)
    cur.close()
    tparams = {
        'title': myresult[0][0],
        'message': 'Your application description page.',
        'year': datetime.now().year,
    }
    return render(request, 'index.html', tparams)

def country(request):
    cur = conn.cursor()
    cur.execute("select country from show_info where id=1;")
    myresult = cur.fetchall()
    #print(myresult)
    cur.close()
    tparams = {
        'title': myresult[0][0],
        'message': 'Your application description page.',
        'year': datetime.now().year,
    }
    return render(request, 'index.html', tparams)

def date_added(request):
    cur = conn.cursor()
    cur.execute("select date_added from show_info where id=1;")
    myresult = cur.fetchall()
    #print(myresult)
    cur.close()
    tparams = {
        'title': myresult[0][0],
        'message': 'Your application description page.',
        'year': datetime.now().year,
    }
    return render(request, 'index.html', tparams)

def release_year(request):
    cur = conn.cursor()
    cur.execute("select release_year from show_info where id=1;")
    myresult = cur.fetchall()
    #print(myresult)
    cur.close()
    tparams = {
        'title': myresult[0][0],
        'message': 'Your application description page.',
        'year': datetime.now().year,
    }
    return render(request, 'index.html', tparams)

def rating(request):
    cur = conn.cursor()
    cur.execute("select rating from show_info where id=1;")
    myresult = cur.fetchall()
    #print(myresult)
    cur.close()
    tparams = {
        'title': myresult[0][0],
        'message': 'Your application description page.',
        'year': datetime.now().year,
    }
    return render(request, 'index.html', tparams)

def duration(request):
    cur = conn.cursor()
    cur.execute("select duration from show_info where id=1;")
    myresult = cur.fetchall()
    #print(myresult)
    cur.close()
    tparams = {
        'title': myresult[0][0],
        'message': 'Your application description page.',
        'year': datetime.now().year,
    }
    return render(request, 'index.html', tparams)

def listed_in(request):
    cur = conn.cursor()
    cur.execute("select listed_in from show_info where id=1;")
    myresult = cur.fetchall()
    #print(myresult)
    cur.close()
    tparams = {
        'title': myresult[0][0],
        'message': 'Your application description page.',
        'year': datetime.now().year,
    }
    return render(request, 'index.html', tparams)

def description(request):
    cur = conn.cursor()
    cur.execute("select description from show_info where id=1;")
    myresult = cur.fetchall()
    #print(myresult)
    cur.close()
    tparams = {
        'title': myresult[0][0],
        'message': 'Your application description page.',
        'year': datetime.now().year,
    }
    return render(request, 'index.html', tparams)