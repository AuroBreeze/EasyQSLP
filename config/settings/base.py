import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Custom apps
    'apps.users',
    'apps.projects',
    'apps.learning',
]

# ... 中间配置保持不变 ...

STATICFILES_DIRS = [str(BASE_DIR / 'static')]
MEDIA_ROOT = str(BASE_DIR / 'media')
MEDIA_URL = '/media/'

# 用户认证配置
AUTH_USER_MODEL = 'users.CustomUser'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'