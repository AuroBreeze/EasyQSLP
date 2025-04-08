from django.db import models

# Create your models here.

class User_login(models.Model):
    username = models.CharField(max_length=20) # 用户名,最大长度为20
    password = models.CharField(max_length=20) # 密码,最大长度为20
    pass
