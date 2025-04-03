FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY requirements /app/requirements
RUN pip install --upgrade pip && \
    pip install -r requirements/prod.txt && \
    pip install gunicorn

COPY . /app

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]