echo "Starting App Port 8000"
python3 -mwebbrowser http://127.0.0.1:8000/
python3 app/src/manage.py runserver 127.0.0.1:8000
