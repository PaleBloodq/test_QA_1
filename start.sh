#!/bin/bash
python manage.py makemigrations 2>&1
python manage.py migrate 2>&1
python manage.py createsuperuser --username admin --email admin@mail.ru --noinput 2>&1
python manage.py runserver 0.0.0.0:8000 2>&1
