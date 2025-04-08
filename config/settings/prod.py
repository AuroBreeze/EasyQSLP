from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test',  # 确保路径正确
        'USER': 'postgres',
        'PASSWORD': 'AuroBreeze',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}