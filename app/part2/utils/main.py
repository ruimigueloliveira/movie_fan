f = open('test3.nt', encoding="utf8")
f2 = open('moviesDB.nt', 'w', encoding="utf8")

director_names = []
actor_names = []
country_names = []
id_movie = 1
str = ''
aspas = 0
ls = []
ls2 = []
for line in f:
    for c in line:
        if c == ',' and aspas == 0:
            ls.append(str)
            str = ''
        elif c == '"' and aspas == 0:
            aspas += 1
        elif c == '"' and aspas == 1:
            aspas -= 1
        if c != ',' or aspas == 1:
            str += c
    ls.append(str.strip())

    type = ls[1].replace('"', '').lower()
    if type == 'tv show':
        type = 'tv_show'
    title = ls[2].replace('"', '')

    str1 = '<http://movies.org/title/{}> <http://movies.org/pred/name> "{}" .'.format(
        id_movie, title)
    str2 = '<http://movies.org/title/{}> <http://movies.org/pred/type> <http://movies.org/en/{}> .'.format(
        id_movie, type)

    f2.write(str1 + '\n' + str2 + '\n')

    # Directors
    if ',' in ls[3]:
        ls_director = ls[3].split(',')
        for elem in ls_director:
            str_director = '<http://movies.org/title/{}> <http://movies.org/pred/directed_by> <http://movies.org/en/{}> .'.format(
                id_movie, elem.strip('"').strip().lower().replace(' ', '_'))
            director_names.append(elem.strip('"').strip())
            f2.write(str_director + '\n')
    else:
        str_director = '<http://movies.org/title/{}> <http://movies.org/pred/directed_by> <http://movies.org/en/{}> .'.format(
            id_movie, ls[3].strip().lower().replace(' ', '_'))
        director_names.append(ls[3].strip())
        f2.write(str_director + '\n')

    # Actors
    if ',' in ls[4]:
        ls_actor = ls[4].split(',')
        for elem in ls_actor:
            str_actor = '<http://movies.org/title/{}> <http://movies.org/pred/starring> <http://movies.org/en/{}> .'.format(
                id_movie, elem.strip('"').strip().lower().replace(' ', '_'))
            actor_names.append(elem.strip('"').strip())
            f2.write(str_actor + '\n')
    else:
        str_actor = '<http://movies.org/title/{}> <http://movies.org/pred/starring> <http://movies.org/en/{}> .'.format(
            id_movie, ls[4].strip().lower().replace(' ', '_'))
        actor_names.append(ls[4].strip())
        f2.write(str_actor + '\n')

    # Country
    if ',' in ls[5]:
        ls_country = ls[5].split(',')
        for elem in ls_country:
            str_country = '<http://movies.org/title/{}> <http://movies.org/pred/country> <http://movies.org/en/{}> .'.format(
                id_movie, elem.strip('"').strip().lower().replace(' ', '_'))
            country_names.append(elem.strip('"').strip())
            f2.write(str_country + '\n')
    else:
        str_country = '<http://movies.org/title/{}> <http://movies.org/pred/country> <http://movies.org/en/{}> .'.format(
            id_movie, ls[5].strip().lower().replace(' ', '_'))
        country_names.append(ls[5].strip())
        f2.write(str_country + '\n')

    date_added = ls[6].replace('"', '')
    release_year = ls[7].replace('"', '')
    rating = ls[8].replace('"', '')
    duration = ls[9].replace('"', '')
    listed_in = ls[10].replace('"', '')
    description = ls[11].replace('"', '')

    str8 = '<http://movies.org/title/{}> <http://movies.org/pred/date_added> "{}" .'.format(
        id_movie, date_added)
    str3 = '<http://movies.org/title/{}> <http://movies.org/pred/release_year> "{}" .'.format(
        id_movie, release_year)
    str4 = '<http://movies.org/title/{}> <http://movies.org/pred/rating> "{}" .'.format(
        id_movie, rating)
    str5 = '<http://movies.org/title/{}> <http://movies.org/pred/duration> "{}" .'.format(
        id_movie, duration)
    str6 = '<http://movies.org/title/{}> <http://movies.org/pred/listed_in> "{}" .'.format(
        id_movie, listed_in)
    str7 = '<http://movies.org/title/{}> <http://movies.org/pred/description> "{}" .'.format(
        id_movie, description)
    id_movie += 1
    f2.write(str8+'\n'+str3+'\n'+str4+'\n'+str5+'\n'+str6+'\n'+str7+'\n')
    ls = []


myset = set(director_names)
for i in myset:
    name_director = '<http://movies.org/en/{}> <http://movies.org/pred/name> "{}" .'.format(i.lower().replace(' ', '_'), i)
    f2.write(name_director + '\n')

myset2 = set(actor_names)
for i in myset2:
    name_actor = '<http://movies.org/en/{}> <http://movies.org/pred/name> "{}" .'.format(i.lower().replace(' ', '_'), i)
    f2.write(name_actor + '\n')

myset3 = set(country_names)
for i in myset3:
    name_country = '<http://movies.org/en/{}> <http://movies.org/pred/name> "{}" .'.format(i.lower().replace(' ', '_'), i)
    f2.write(name_country + '\n')


f2.write('<http://movies.org/en/tv_show> <http://movies.org/pred/name> "TV Show" .\n')
f2.write('<http://movies.org/en/movie> <http://movies.org/pred/name> "Movie" .\n')
f2.close()
f.close()
