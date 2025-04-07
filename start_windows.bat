@echo off
call .venv\Scripts\activate
python manage.py runserver --settings=config.settings.base
pause