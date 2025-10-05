from django.urls import path,include
from . import views

#指定应用名称(命名空间)
app_name='api'


urlpatterns=[
    path('user/',include("apps.user.api.urls"),name="api_user"),
    path('project/',include("apps.projectmanage.manage.urls"),name="api_project"),
]