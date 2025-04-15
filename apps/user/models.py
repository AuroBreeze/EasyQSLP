from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
#验证器
# MinLengthValidator(5) 表示最小长度为5
# MaxLengthValidator(25) 表示最大长度为25
# EmailValidator() 表示验证是否为邮箱格式
# MinValueValidator(18) 表示最小值为18
# MaxValueValidator(100) 表示最大值为100
# URLValidator() 表示验证是否为网址格式
# RegexValidator(r'^[a-zA-Z0-9_-]{5,20}$') 表示验证是否为字母、数字、下划线、减号组成的字符串，长度为5到20
from django.core.validators import MinLengthValidator
# Create your models here.
class UserRegisterManager(BaseUserManager):
    """
    自定义用户注册管理器
    """
    def create(self,email,username,password):
        if not email:
            raise ValueError({"email":"邮箱不能为空"})
        if not username:
            raise ValueError({"username":"用户名不能为空"})
        if not password:
            raise ValueError({"password":"密码不能为空"})

        return self.model(
            email=self.normalize_email(email),
            username=username,
            password=make_password(password)
            )
    def create_user(self,email,username,password,is_active):
        user = self.create(email,username,password)
        user.is_active = is_active
        user.save()
        return user

class User_Login(AbstractBaseUser): #正常django会生成一个 app名_类名 的表名
    username = models.CharField(max_length=20,validators=[MinLengthValidator(5)],unique=True)
    password = models.CharField(max_length=255)#最大长度要保证哈希后的长度能够放进数据库
    join_date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=50,unique=True)
    is_active = models.BooleanField(default=True) #是否激活
    #uuid_user = models.UUIDField(default=uuid4,editable=False,unique=True) #用户唯一标识符
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserRegisterManager() #用户注册管理器
    
    # def get_by_natural_key(self,email):
    #     return self.get(email=email)
    class Meta: #指定元数据，固定写法
        db_table = 'user_login' #指定表名
        
        #先按join_date降序排序，再按username升序排序
        #ordering = ['-join_date','username'] #指定默认排序字段,加‘-’表示降序排序
    #用户注册

class Email_Verify_Code(models.Model):
    email = models.EmailField(max_length=50,unique=True,verbose_name='用户标识')
    code = models.CharField(max_length=6,verbose_name='验证码')
    send_time = models.DateTimeField(auto_now_add=True,verbose_name='发送时间')
    expire_time = models.DateTimeField(verbose_name='过期时间')
    class Meta:
        db_table = 'email_verify_code'
        verbose_name = '邮箱验证码'
        verbose_name_plural = '邮箱验证码'

    def __str__(self):
        return f"{self.email} - {self.code}"
class User_Profile(models.Model):
    profile_text = models.TextField(max_length=500,default='')
    
    #user = models.ForeignKey('User_Login',on_delete=models.CASCADE) #外键关联到User_Login表

class Article(models.Model): #一对多关系
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    
    # on_delete=models.CASCADE 表示当Article表中的数据被删除时，关联的User_Login表中的数据也会被删除
    # on_delete=models.SET_NULL 表示当Article表中的数据被删除时，关联的User_Login表中的数据的值设置为null
    # on_delete=models.PROTECT 表示如果Article表中的数据被删除，则User_Login表中的数据也不能被删除
    # on_delete=models.DO_NOTHING 表示当Article表中的数据被删除时，关联的User_Login表中的数据的值不进行任何处理
    
    # related_name='articles' 表示在User_Login表中的articles字段表示关联到Article表的数据
    author = models.ForeignKey('User_Login',on_delete=models.CASCADE,related_name='articles') #外键关联到User_Login表
    
class UserExtension(models.Model):
    birthday = models.DateField(null=True)
    school = models.CharField(max_length=50,null=True)
    
    # 一对一关系
    user = models.OneToOneField('User_Login',on_delete=models.CASCADE,related_name='extension')

class ArticleTag(models.Model):
    name = models.CharField(max_length=20)
    
    # 多对多关系
    articles = models.ManyToManyField('Article',related_name='tags')

class Comment(models.Model):
    content = models.TextField(max_length=500)
    
    # 二级评论 外键关联到Comment表
    original_comment = models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    
    