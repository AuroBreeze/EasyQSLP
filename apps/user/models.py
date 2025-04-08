from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.

class User_Login(models.Model):
    username = models.CharField(max_length=20,validators=[MinLengthValidator(5)],unique=True)
    password = models.CharField(max_length=25)
    join_date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=50,unique=True)
    