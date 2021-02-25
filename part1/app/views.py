import requests
import xmltodict
from BaseXClient import BaseXClient
from django.http import Http404, HttpRequest
from django.shortcuts import render
from djangoProject2.settings import BASE_DIR
import os
from lxml import etree
from datetime import date


# Open session
session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
session.execute("open streamData")
DBname = 'streamData.xml'
pname = os.path.join(BASE_DIR, 'app/data/' + DBname)

#XSD
xsdfile = etree.parse(os.path.join(BASE_DIR, 'app/data/streamData.xsd'))
xsd = etree.XMLSchema(xsdfile)

xml = etree.parse(pname)
xmlError = etree.parse(os.path.join(BASE_DIR, 'app/data/streamDataError.xml'))

# Update DataBase (Watched atribute)


# Home Page
def home_page(request):
    input_shows_title = "import module namespace funcs = 'com.funcs.my.index' at '" \
                         + os.path.join(BASE_DIR, 'app/queries/return_shows.xq') + "'; " \
                         "funcs:return_shows()"

    input_shows_id = "import module namespace funcs = 'com.funcs.my.index' at '" \
                      + os.path.join(BASE_DIR, 'app/queries/return_shows_id.xq') + "'; " \
                        "funcs:return_shows_id()"

    input_shows_watched = "import module namespace funcs = 'com.funcs.my.index' at '" \
                     + os.path.join(BASE_DIR, 'app/queries/return_shows_watched.xq') + "'; " \
                                                                                  "funcs:return_shows_watched()"


    dict = ls_to_dict3(input_shows_title, input_shows_id, input_shows_watched)
    tparams = {
        'programas': dict,

    }
    return render(request, 'home_page.html', tparams)


# Programa em que carregamos
def filme(request):
    if not 'show_id' in request.GET:
        raise Http404("Filme não disponível!")
    id = request.GET['show_id']

    info = get_full_info(id)

    tparams = {
        'filme': info,
    }

    return render(request, 'filme.html', tparams)


# Lista de todos os filmes
def movieslist(request):
    tparams = load_movies()
    return render(request, 'movieslist.html', tparams)


# Lista de todas as series
def serieslist(request):
    tparams = load_show()
    return render(request, 'serieslist.html', tparams)


# Filtrar programas por país onde foram feitos
def program_from_country(request, country):
    # Title
    input_countries_1 = "import module namespace funcs = 'com.funcs.my.index' at '" \
             + os.path.join(BASE_DIR, 'app/queries/id_by_country.xq') + "'; " \
             "funcs:show_id_by_country('" + country + "')"

    # Id
    input_countries_2 = "import module namespace funcs = 'com.funcs.my.index' at '" \
             + os.path.join(BASE_DIR, 'app/queries/title_by_country.xq') + "'; " \
             "funcs:show_title_by_country('" + country + "')"

    # Watched
    input_countries_3 = "import module namespace funcs = 'com.funcs.my.index' at '" \
                        + os.path.join(BASE_DIR, 'app/queries/watched_by_country.xq') + "'; " \
                        "funcs:watched_by_country('" + country + "')"

    # Converter as duas listas num dicionário
    dict = ls_to_dict3(input_countries_1, input_countries_2, input_countries_3)

    tparams = {
        'programas': dict,
    }

    return render(request, 'program_from_country.html', tparams)


def add_movie(request):
    assert isinstance(request, HttpRequest)
    if 'title' in request.POST:
        info = dict()
        info['show_id'] = get_new_id()
        info['title'] = request.POST['title']
        info['type'] = request.POST['type']
        info['director'] = request.POST['director']
        info['cast'] = request.POST['cast']
        info['country'] = request.POST['country']
        info['release_year'] = request.POST['release_year']
        info['rating'] = request.POST['rating']
        info['duration'] = request.POST['duration']
        info['listed_in'] = request.POST['listed_in']
        info['description'] = request.POST['description']
        info['date_added'] = date.today().strftime("%B %d, %Y")
        info['watched'] = 'False'
        for k, v in info.items():
            if v == '':
                info[k] = 'Unknown'

        info['title'] = info['title'][0].upper() + info['title'][1:]
        if info['title']:
            input = "import module namespace funcs = 'com.funcs.my.index' at '" \
                     + os.path.join(BASE_DIR, 'app/queries/new_movie.xq') + "'; " \
                     "funcs:new_movie('" + info['show_id'] + "', '" + info['type'] + "', '"\
                     + info['title'] + "', '" + info['director'] + "', '" + info['cast'] + "', '" \
                     + info['country'] + "', '" + info['date_added'] + "', '" + info['release_year'] + "', '" \
                     + info['rating'] + "', '" + info['duration'] + "', '" + info['listed_in'] + "', '" \
                     + info['description'] + "', '" + info['watched'] + "')"
            session.query(input).execute()
            tparams = {
                'filme': info,
            }
            return render(request, 'filme.html', tparams)
        else:
            return render(request, 'movieslist.html', {'Error': True, })
    else:
        return render(request, 'add_movie.html', {'Error': False, })


def delete_movie(request):
    id = request.GET['show_id']
    query = "import module namespace funcs = 'com.funcs.my.index' at '" \
            + os.path.join(BASE_DIR, 'app/queries/delete_movie.xq') + "'; " \
            "funcs:delete_movie('" + id + "')"
    delete = session.query(query).execute()

    tparams = load_movies()
    return render(request, 'movieslist.html', tparams)


def add_rating_1(request):
    id = request.GET['show_id']
    tparams = add_rating(id, '1')
    return render(request, 'filme.html', tparams)

def add_rating_2(request):
    id = request.GET['show_id']
    tparams = add_rating(id, '2')
    return render(request, 'filme.html', tparams)

def add_rating_3(request):
    id = request.GET['show_id']
    tparams = add_rating(id, '3')
    return render(request, 'filme.html', tparams)

def add_rating_4(request):
    id = request.GET['show_id']
    tparams = add_rating(id, '4')
    return render(request, 'filme.html', tparams)

def add_rating_5(request):
    id = request.GET['show_id']
    tparams = add_rating(id, '5')
    return render(request, 'filme.html', tparams)


def has_watched(request):
    id = request.GET['show_id']
    mark_as_watched = "import module namespace funcs = 'com.funcs.my.index' at '" \
                      + os.path.join(BASE_DIR, 'app/queries/add_as_watched.xq') + "'; " \
                      "funcs:add_as_watched('" + id + "', 'True')"

    session.query(mark_as_watched).execute()

    info = get_full_info(id)
    tparams = {
        'filme': info,
    }
    return render(request, 'filme.html', tparams)


def has_not_watched(request):
    id = request.GET['show_id']
    mark_as_not_watched = "import module namespace funcs = 'com.funcs.my.index' at '" \
                      + os.path.join(BASE_DIR, 'app/queries/add_as_watched.xq') + "'; " \
                      "funcs:add_as_watched('" + id + "', 'False')"

    session.query(mark_as_not_watched).execute()
    info = get_full_info(id)
    tparams = {
        'filme': info,
    }
    return render(request, 'filme.html', tparams)


def userprofile(request):
    xsltfilename = 'user_profile.xsl'
    xsltfile = os.path.join(BASE_DIR, 'app/data/' + xsltfilename)
    xsl = etree.parse(xsltfile)
    transform = etree.XSLT(xsl)

    query_all_db = "import module namespace funcs = 'com.funcs.my.index' at '" \
                   + os.path.join(BASE_DIR, 'app/queries/all_db.xq') + "'; " \
                   "funcs:all_db()"

    shows = "<root>" + session.query(query_all_db).execute() + "</root>"

    root = etree.fromstring(shows)

    info = dict()
    info = transform(root)

    tparams = {
        'content': info,
    }

    return render(request, 'userprofile.html', tparams)


# RSS feed
def news(request):
    xsltfilename = 'rss_info.xsl'
    xsltfile = os.path.join(BASE_DIR, 'app/data/' + xsltfilename)
    xsl = etree.parse(xsltfile)
    transform = etree.XSLT(xsl)

    url = 'https://www.cinemablend.com/rss/topic/news/movies'
    resp = requests.get(url)

    rss = etree.fromstring(resp.content)
    html = transform(rss)

    tparams = {
        'content': html,
    }

    return render(request, 'rss_feed.html', tparams)


# Função para verificar se o ficheiro XML é válido
def verify_xml(request):
    assert isinstance(request, HttpRequest)
    if 'xmlfile' in request.POST:
        info = dict()
        xmlName = request.POST['xmlfile']
        if xmlName == 'streamData.xml':
            info['verifica'] = xsd.validate(xml)
        else:
            info['verifica'] = xsd.validate(xmlError)
        tparams = {
            'imprimir': info,
        }
        return render(request, 'returnverify.html', tparams)
    else:
        return render(request, 'verifyxml.html', {'Error': False, })


# Aux Functions
def ls_to_dict(ls_1, ls_2):
    query_1 = session.query(ls_1).execute()
    query_2 = session.query(ls_2).execute()

    ls1 = query_1.split('\n')
    ls2 = query_2.split('\n')
    dictionary = {ls2[i]: ls1[i] for i in range(len(ls2))}

    return dictionary


# Converts 3 list into a dictionary of tuples
def ls_to_dict3(ls_1, ls_2, ls_3):
    query_1 = session.query(ls_1).execute()
    query_2 = session.query(ls_2).execute()
    query_3 = session.query(ls_3).execute()

    ls1 = query_1.split('\n')
    ls2 = query_2.split('\n')
    ls3 = query_3.split('\n')
    dct = {ls2.strip(): {ls1.strip(): ls3.strip()} for ls2, ls1, ls3 in zip(ls2, ls1, ls3)}
    return dct


# Retorna o valor do id disponível para o novo filme
def get_new_id():
    last_id = "import module namespace funcs = 'com.funcs.my.index' at '" \
            + os.path.join(BASE_DIR, 'app/queries/ret_showid_numb.xq') + "'; " \
            "funcs:ret_showid_numb()"
    id = session.query(last_id).execute()

    return str(int(id) + 1)


def load_movies():
    input_movies_title = "import module namespace funcs = 'com.funcs.my.index' at '" \
                         + os.path.join(BASE_DIR, 'app/queries/show_movies.xq') + "'; " \
                                                                                  "funcs:show_movies()"

    input_movies_id = "import module namespace funcs = 'com.funcs.my.index' at '" \
                      + os.path.join(BASE_DIR, 'app/queries/show_movies_id.xq') + "'; " \
                                                                                  "funcs:show_movies_id()"

    input_shows_watched = "import module namespace funcs = 'com.funcs.my.index' at '" \
                          + os.path.join(BASE_DIR, 'app/queries/show_movies_watched.xq') + "'; " \
                          "funcs:show_movies_watched()"

    #input_shows_rating = "import module namespace funcs = 'com.funcs.my.index' at '" \
    #                      + os.path.join(BASE_DIR, 'app/queries/show_movies_rating.xq') + "'; " \
    #                      "funcs:show_movies_rating()"

    dict = ls_to_dict3(input_movies_title, input_movies_id, input_shows_watched)
    tparams = {
        'programas': dict,
    }
    return tparams


def load_show():
    input_series_title = "import module namespace funcs = 'com.funcs.my.index' at '" \
                         + os.path.join(BASE_DIR, 'app/queries/show_series.xq') + "'; " \
                                                                                  "funcs:show_series()"

    input_series_id = "import module namespace funcs = 'com.funcs.my.index' at '" \
                      + os.path.join(BASE_DIR, 'app/queries/show_series_id.xq') + "'; " \
                                                                                  "funcs:show_series_id()"

    input_series_watched = "import module namespace funcs = 'com.funcs.my.index' at '" \
                          + os.path.join(BASE_DIR, 'app/queries/show_series_watched.xq') + "'; " \
                                                                                           "funcs:show_series_watched()"
    dict = ls_to_dict3(input_series_title, input_series_id, input_series_watched)
    tparams = {
        'programas': dict,
    }
    return tparams


def get_full_info(id):
    movie = "import module namespace funcs = 'com.funcs.my.index' at '" \
            + os.path.join(BASE_DIR, 'app/queries/return_movie.xq') + "'; " \
            "funcs:return_movie('" + id + "')"
    query = session.query(movie).execute()
    if query is None:
        raise Http404("Filme não disponível!")

    ls = query.split('\n')
    info = dict()
    info['show_id'] = ls[0].strip()
    info['type'] = ls[1].strip()
    info['title'] = ls[2].strip()
    info['director'] = ls[3].strip()
    info['cast'] = ls[4].strip()
    info['country'] = ls[5].strip()
    info['date_added'] = ls[6].strip()
    info['release_year'] = ls[7].strip()
    info['rating'] = ls[8].strip()
    info['duration'] = ls[9].strip()
    info['listed_in'] = ls[10].strip()
    info['description'] = ls[11].strip()
    info['watched'] = ls[12].strip()
    if len(ls) is 14:
        info['valuation'] = ls[13].strip()
    return info


def add_rating(id, rating):
    rate = "import module namespace funcs = 'com.funcs.my.index' at '" \
                      + os.path.join(BASE_DIR, 'app/queries/add_rating.xq') + "'; " \
                      "funcs:add_rating('" + id + "', '" + rating + "')"

    session.query(rate).execute()

    info = get_full_info(id)
    tparams = {
        'filme': info,
    }
    return tparams
