f = open('test.nt', encoding="utf8")
f2 = open('test2.nt', 'w', encoding="utf8")

ls = []
for line in f:
    if '<http://movies.org/pred/listed_in>' in line:
        prov_ls = line.split('>')
        original = prov_ls[0]
        categories = prov_ls[2].strip().split('"')[1]
        if categories == "Kids' TV":
            categories = 'Kids TV'
        if ',' in categories:
            categories_ls = categories.split(',')
            for c in categories_ls:
                if c == "Kids' TV":
                    c = "Kids TV"
                ls.append(c.strip())
                line = '{}> <http://movies.org/pred/listed_in> <http://movies.org/en/{}> .'.format(original, c.strip().lower().replace(' ', '_'))
                f2.write(line + '\n')
        else:
            ls.append(categories)
            line = '{}> <http://movies.org/pred/listed_in> <http://movies.org/en/{}> .'.format(original, categories.strip().lower().replace(' ', '_'))
            f2.write(line + '\n')
    else:
        f2.write(line)

myset = set(ls)

for i in myset:
    name_category = '<http://movies.org/en/{}> <http://movies.org/pred/name> "{}" .'.format(i.lower().replace(' ', '_'), i)
    f2.write(name_category + '\n')
f.close()
f2.close()
