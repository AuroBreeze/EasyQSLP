from django.urls import path
from .views import *

# 指定应用名称(命名空间)
app_name = 'user'

urlpatterns = [
    path("login/", LoginAPI.as_view(), name="login"), # 登录
    path("register/", RegisterAPI.as_view(), name="register"), # 注册
    path("querr/", Querr.as_view(), name="querr"),
    path("article/", ArticleAPI.as_view(), name="article"),
    path("articlelist/", ArticleListAPI.as_view(), name="articlelist"),
    path("emailsendcode/", EmailCodeSendAPI.as_view(), name="emailsendcode"), # 发送邮箱验证码
    path("resetpassword/", ResetPasswordAPI.as_view(), name="restpassword") # 重置密码
]