chcp 65001
@echo off
call .venv\Scripts\activate
python manage.py runserver
pause