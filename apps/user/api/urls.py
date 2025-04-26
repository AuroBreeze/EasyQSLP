from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
# 指定应用名称(命名空间)
app_name = 'user'

urlpatterns = [
    path("login/", LoginAPI.as_view(), name="login"), # 登录
    path("register/", RegisterAPI.as_view(), name="register"), # 注册
    # path("querr/", Querr.as_view(), name="querr"),
    # path("article/", ArticleAPI.as_view(), name="article"),
    # path("articlelist/", ArticleListAPI.as_view(), name="articlelist"),
    path("emailsendcode/", EmailCodeSendAPI.as_view(), name="emailsendcode"), # 发送邮箱验证码
    path("resetpassword/", ResetPasswordAPI.as_view(), name="restpassword"), # 重置密码

    path("token/", UserTokenObtainPairAPI.as_view(), name="token"), # JWT认证获取
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"), # JWT认证刷新
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"), # JWT认证验证

    path("profile/revise/", UserProfileAPI.as_view(), name="revise-profile"),
    path("profile/<int:pk>/", UserProfileAPI.as_view(), name="user-profile")

]