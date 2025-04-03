from .base import *

# 根据环境变量加载不同配置
env = os.environ.get('DJANGO_ENV', 'development')

if env == 'production':
    from .production import *
else:
    from .development import *