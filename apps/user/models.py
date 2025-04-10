from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.

class User_Login(models.Model): #正常django会生成一个 app名_类名 的表名
    username = models.CharField(max_length=20,validators=[MinLengthValidator(5)],unique=True)
    password = models.CharField(max_length=25)
    join_date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=50,unique=True,default='')
    class Meta: #指定元数据，固定写法
        db_table = 'user_login' #指定表名
        
        #先按join_date降序排序，再按username升序排序
        #ordering = ['-join_date','username'] #指定默认排序字段,加‘-’表示降序排序

class User_Profile(models.Model):
    profile_text = models.TextField(max_length=500,default='')
    
    #user = models.ForeignKey('User_Login',on_delete=models.CASCADE) #外键关联到User_Login表

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    
    # on_delete=models.CASCADE 表示当Article表中的数据被删除时，关联的User_Login表中的数据也会被删除
    # on_delete=models.SET_NULL 表示当Article表中的数据被删除时，关联的User_Login表中的数据的值设置为null
    # on_delete=models.PROTECT 表示如果Article表中的数据被删除，则User_Login表中的数据也不能被删除
    # on_delete=models.DO_NOTHING 表示当Article表中的数据被删除时，关联的User_Login表中的数据的值不进行任何处理
    
    # related_name='articles' 表示在User_Login表中的articles字段表示关联到Article表的数据
    author = models.ForeignKey('User_Login',on_delete=models.CASCADE,related_name='articles') #外键关联到User_Login表

class Comment(models.Model):
    content = models.TextField(max_length=500)
    
    # 二级评论 外键关联到Comment表
    original_comment = models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    
    