import requests

url = 'http://127.0.0.1:8000/v1/movie/rank'
myobj = {'show_id':3771, 'rank': 5}

x = requests.post(url, data = myobj)