pip install -r requirements.txt 
python manage.py collectstatic --no-input 
python manage.py migrate 
gunicorn -w 1 -t 180 -b unix:/socket/fblog.sock fblog.wsgi
