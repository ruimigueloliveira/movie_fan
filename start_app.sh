echo Instaling requirements:
pip install -r app/src/requirements.txt

echo $'\n'$'\n'Starting App Port 8000:
python3 app/src/manage.py runserver 0.0.0.0:8000
