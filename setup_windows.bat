@echo off
python -m venv .venv
call .venv\Scripts\activate
python -m pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python seed_demo.py
python manage.py runserver
