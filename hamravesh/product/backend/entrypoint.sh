#!/bin/bash

echo "make-migrations & migrate"
python manage.py makemigrations
python manage.py migrate

echo "collecting statics"
python manage.py collectstatic --no-input

# echo "stating wsgi gunicorn server"
# gunicorn core.wsgi:application --bind "0.0.0.0:8000" --daemon

# echo "Starting ASGI server..."
# daphne -b 0.0.0.0 -p 8000 core.asgi:application

echo "starting asgi gunicorn server"
python -m gunicorn --bind 0.0.0.0:8000  core.asgi:application -k uvicorn.workers.UvicornWorker --daemon

echo "starting nginx server"
nginx -g 'daemon off;'
