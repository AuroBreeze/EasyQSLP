@echo off
call .venv\Scripts\activate
python manage.py runserver --settings=config.settings.dev
pause