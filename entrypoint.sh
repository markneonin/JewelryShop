#! /bin/bash

cd JewelryShop

python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input

exec gunicorn JewelryShop.wsgi --bind 0.0.0.0:8000 --reload