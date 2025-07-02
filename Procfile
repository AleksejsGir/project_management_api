web: gunicorn project_management.wsgi --bind 0.0.0.0:$PORT --log-file -
release: python manage.py migrate --settings=project_management.production_settings