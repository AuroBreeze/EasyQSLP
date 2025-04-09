from django.urls import path
from .views import *

#指定应用名称(命名空间)
app_name='user'


urlpatterns=[
    path("login/",LoginAPI.as_view(),name="login"),
    path("register/",RegisterAPI.as_view(),name="register"),
    path("querr/",Querr.as_view(),name="querr"),
    path("article/",ArticleAPI.as_view(),name="article")
]