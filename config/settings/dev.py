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
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'apps.user.apps.UserConfig',
    'apps.projectmanage.apps.ProjectmanageConfig',  # 确保应用路径正确
    'apps.api.apps.ApiConfig'
]

# 确保 INSTALLED_APPS_DEV 在 INSTALLED_APPS 之前
INSTALLED_APPS = INSTALLED_APPS + INSTALLED_APPS_DEV


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

# Markdown 扩展
MARKDOWN_EXTENSIONS = [
    'markdown.extensions.extra',
    'markdown.extensions.codehilite',
    'markdown.extensions.toc',
    'mdx_math'
]

# 缓存配置
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# 代码高亮样式
PYGMENTS_STYLE = 'monokai'


#celery配置
CELERY_BROKER_URL = 'redis://localhost:6379/0'#broker地址
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'#结果存储地址
CELERY_ACCEPT_CONTENT = ['json']#指定接受的内容类型
CELERY_TASK_SERIALIZER = 'json'#任务序列化和反序列化方案
CELERY_TIMEZONE = 'Asia/Shanghai'#时区

# JWT配置
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # 启用 JWT 认证
    ),
}
from django.utils import timezone

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timezone.timedelta(minutes=30),  # 访问令牌有效期（示例：30分钟）
    'REFRESH_TOKEN_LIFETIME': timezone.timedelta(minutes=60),     # 刷新令牌有效期（示例：1小时）
    'ROTATE_REFRESH_TOKENS': True,                   # 刷新令牌后是否生成新令牌
    'BLACKLIST_AFTER_ROTATION': True,                # 旧刷新令牌是否加入黑名单
    'ALGORITHM': 'HS256',                            # 加密算法
    'SIGNING_KEY': SECRET_KEY,                        # 使用 Django 的 SECRET_KEY 作为签名密钥
}

from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'clear_expired_codes': {
        'task': 'apps.user.task.clear_expired_codes_task',
        'schedule': crontab(minute='*/30'),
    },
}


from bleach.sanitizer import Cleaner

cleaner = Cleaner(
    tags=[
        'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol',
        'strong', 'ul', 'pre', 'p', 'br', 'hr', 'img', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'table', 'thead', 'tbody', 'tr', 'th', 'td', 'span', 'div', 'kbd', 'samp', 'sub', 'sup'
    ],
    attributes={
        '*': ['class', 'id', 'title', 'align', 'style'],
        'a': ['href', 'title', 'rel'],
        'img': ['src', 'alt', 'title', 'width', 'height'],
        'th': ['colspan', 'rowspan'],
        'td': ['colspan', 'rowspan'],
    },
    protocols=['http', 'https', 'mailto', 'data'],
    strip=True,
    strip_comments=True
)


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

