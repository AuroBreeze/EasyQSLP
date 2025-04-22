from .base import *

DEBUG = True

# 允许的请求方法
CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'OPTIONS',  # 必须包含OPTIONS
]

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 安装的应用
INSTALLED_APPS_DEV = [
    'corsheaders',
    'apps.user.apps.UserConfig'
    'apps.projectmanage.apps.ProjectmanageConfig'
]

INSTALLED_APPS = INSTALLED_APPS_DEV + INSTALLED_APPS


# 静态文件配置
MEDIA_ROOT = BASE_DIR.parent / 'media'  # 媒体文件存储路径

# 禁用安全警告（仅开发环境！）
SECURE_HSTS_SECONDS = 0  # 禁用HSTS
SECURE_SSL_REDIRECT = False  # 不强制HTTPS
SESSION_COOKIE_SECURE = False  # 允许HTTP传输Cookie
CSRF_COOKIE_SECURE = False  # 允许HTTP传输CSRF Token



# 登录配置
AUTH_USER_MODEL = 'user.User_Login'  # 替换 your_app 为实际应用名
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # 默认后端（支持 USERNAME_FIELD）
]

# 跨域配置
ALLOWED_HOSTS = ['localhost','localhost:7856', '127.0.0.1:7856','127.0.0.1:20000','127.0.0.1']  # 开发环境允许的域名
CORS_ORIGIN_WHITELIST = (
    'http://localhost:7856',
    'http://127.0.0.1:7856',
    'http://127.0.0.1:20000'
)  # 允许跨域请求的域名

#celery配置
CELERY_BROKER_URL = 'redis://localhost:6379/0'#broker地址
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'#结果存储地址
CELERY_ACCEPT_CONTENT = ['json']#指定接受的内容类型
CELERY_TASK_SERIALIZER = 'json'#任务序列化和反序列化方案
CELERY_TIMEZONE = 'Asia/Shanghai'#时区

from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'clear_expired_codes': {
        'task': 'apps.user.task.clear_expired_codes_task',
        'schedule': crontab(minute='*/30'),
    },
}


# 邮箱配置
import toml

# 读取配置文件
try:
    config_env = toml.load(BASE_DIR.parent / './config_env.toml')

except FileNotFoundError:
    raise FileNotFoundError('config.toml文件不存在')

# 邮箱配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config_env["EMAIL"]["HOST"]
EMAIL_PORT = config_env["EMAIL"]["PORT"]
EMAIL_USE_SSL = True
#EMAIL_USE_TLS = True
EMAIL_HOST_USER = config_env["EMAIL"]["USER"]
EMAIL_HOST_PASSWORD = config_env["EMAIL"]["PASSWORD"]

