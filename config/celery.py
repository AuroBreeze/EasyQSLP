import os
from celery import Celery

#设置Django环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE","config.settings.dev")

# 创建celery实例
app = Celery("EasyQFLP")

# 加载celery配置
app.config_from_object("config.settings.dev",namespace="CELERY")

# 自动发现任务
app.autodiscover_tasks()