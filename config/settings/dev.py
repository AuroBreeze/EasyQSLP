from .base import *

DEBUG = True

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
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
INSTALLED_APPS_DEV = [
    'apps.user.apps.UserConfig'
]

INSTALLED_APPS = INSTALLED_APPS_DEV + INSTALLED_APPS

MEDIA_ROOT = BASE_DIR.parent / 'media'  # 媒体文件存储路径

# 禁用安全警告（仅开发环境！）
SECURE_HSTS_SECONDS = 0  # 禁用HSTS
SECURE_SSL_REDIRECT = False  # 不强制HTTPS
SESSION_COOKIE_SECURE = False  # 允许HTTP传输Cookie
CSRF_COOKIE_SECURE = False  # 允许HTTP传输CSRF Token
ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # 开发环境允许的域名

# 生成随机密钥（运行后复制到配置中）
# from django.core.management.utils import get_random_secret_key
# print(f"SECRET_KEY = '{get_random_secret_key()}'")  # 运行后替换下面的值
# SECRET_KEY = '你的新密钥'  # 替换为打印出来的随机值


AUTH_USER_MODEL = 'user.User_Login'  # 替换 your_app 为实际应用名
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # 默认后端（支持 USERNAME_FIELD）
]