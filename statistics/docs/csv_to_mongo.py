import csv
import pymongo

client = pymongo.MongoClient("localhost", 27017)
db = client.movies
with open('movies.csv', 'r') as f:

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
