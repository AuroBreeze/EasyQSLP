from django.urls import path
from . import views

#指定应用名称(命名空间)
app_name='api'


urlpatterns=[
    path('user_login',views.user_login,name='user_login')
]