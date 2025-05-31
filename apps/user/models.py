from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
#验证器
# MinLengthValidator(5) 表示最小长度为5
# MaxLengthValidator(25) 表示最大长度为25
# EmailValidator() 表示验证是否为邮箱格式
# MinValueValidator(18) 表示最小值为18
# MaxValueValidator(100) 表示最大值为100
# URLValidator() 表示验证是否为网址格式
# RegexValidator(r'^[a-zA-Z0-9_-]{5,20}$') 表示验证是否为字母、数字、下划线、减号组成的字符串，长度为5到20
from django.core.validators import MinLengthValidator
import random
from django.utils import timezone
# Create your models here.
class UserRegisterManager(BaseUserManager):
    """
    自定义用户注册管理器
    """
    def create(self,email,username,password):#type:ignore
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
    def create_user(self,email,username,password,**extra_fields):
        user = self.create(email,username,password)
        user.is_active = True
        if extra_fields:
            for key, value in extra_fields.items():
                setattr(user, key, value)
        else:
            user.is_staff = False
            user.is_superuser = False
        user.save()
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        """
        创建超级用户的专用方法
        注意：参数顺序要与USERNAME_FIELD和REQUIRED_FIELDS对应
        """
        # 设置管理员默认权限
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        # 验证权限字段
        if extra_fields.get('is_staff') is not True:
            raise ValueError('超级用户必须设置 is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('超级用户必须设置 is_superuser=True')

        return self.create_user(email, username, password, **extra_fields)
        
class EmailCodeSendManager(models.Manager):
    def create(self,email): #type:ignore
        if not email:
            raise ValueError({"email":"邮箱不能为空"})
        code = "".join(random.choices('0123456789', k=6))
        send_time = timezone.now()
        expire_time = send_time + timezone.timedelta(minutes=5) #type:ignore
        usage = "Register"
        
        return self.model(
            email=email,
            code=code,
            send_time=send_time,
            expire_time=expire_time,
            usage=usage
        )

class User_Login(AbstractBaseUser,PermissionsMixin): #正常django会生成一个 app名_类名 的表名
    username = models.CharField(max_length=20,validators=[MinLengthValidator(5)],unique=True,verbose_name='用户名')
    password = models.CharField(max_length=255,verbose_name='密码')#最大长度要保证哈希后的长度能够放进数据库
    join_date = models.DateTimeField(auto_now_add=True,verbose_name='注册日期')
    last_login = models.DateTimeField(auto_now=True,verbose_name='上次登录日期')
    email = models.EmailField(max_length=50,unique=True,verbose_name='邮箱')
    is_active = models.BooleanField(default=True,verbose_name='是否激活') #是否激活
    
    #uuid_user = models.UUIDField(default=uuid4,editable=False,unique=True) #用户唯一标识符
    # 权限相关字段
    is_staff = models.BooleanField(
        default=False,
        verbose_name="管理员权限",
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name="超级管理员权限"
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserRegisterManager() #用户注册管理器
    
    # def get_by_natural_key(self,email):
    #     return self.get(email=email)
    class Meta: #指定元数据，固定写法
        db_table = 'user_login' #指定表名
        verbose_name = '用户登录管理'
        verbose_name_plural = '用户登录管理'
        
        #先按join_date降序排序，再按username升序排序
        #ordering = ['-join_date','username'] #指定默认排序字段,加‘-’表示降序排序
    #用户注册

class Email_Verify_Code(models.Model):
    email = models.EmailField(max_length=50,unique=True,verbose_name='用户标识')
    code = models.CharField(max_length=6,verbose_name='验证码')
    send_time = models.DateTimeField(verbose_name='发送时间',)
    expire_time = models.DateTimeField(verbose_name='过期时间/s')
    usage = models.CharField(max_length=25,verbose_name='用途',default='Register')
    
    objects = EmailCodeSendManager() #验证码管理器

    def is_expired(self):
        return timezone.now() > self.expire_time #5分钟过期

    class Meta:
        db_table = 'email_verify_code'
        verbose_name = '邮箱验证码'
        verbose_name_plural = '邮箱验证码'

    def __str__(self):
        return f"{self.email} - {self.code}"

    
class User_Profile(models.Model):

    avatar = models.ImageField(upload_to='avatar/',null=True,default='avatar/default.png',verbose_name='头像')
    
    userprofile_md = models.TextField(verbose_name='个人资料markdown') #存储原始markdown
    userprofile_html = models.TextField(verbose_name='个人资料html',editable=False)  # 自动生成的 HTML #存储渲染后的html
    content_hash = models.CharField(max_length=32, editable=False)  # 用于缓存校验
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    
    user_Login = models.ForeignKey('User_Login',on_delete=models.CASCADE,related_name='profile') #外键关联到User_Login表

    def save(self, *args, **kwargs):

        if not self.content_hash or self.has_content_changed():
            self.content_html = self.generate_safe_html()
            self.content_hash = self.calculate_hash()
        super().save(*args, **kwargs)

    def has_content_changed(self):
        if not self.pk:
            return True
        old = User_Profile.objects.get(pk=self.pk)
        return self.content_md != old.content_md

    def generate_safe_html(self):
        from markdown import markdown
        from bleach.sanitizer import Cleane
        # 生成基础 HTML
        html = markdown(
            self.content_md,
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
                'mdx_math'  # 需要安装 python-markdown-math
            ]
        )

        # 安全清理
        cleaner = Cleaner(
            tags=[
                'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                'ul', 'ol', 'li', 'p', 'br',
                'strong', 'em', 'code', 'pre', 'blockquote',
                'table', 'thead', 'tbody', 'tr', 'th', 'td',
                'a', 'img', 'span', 'div'
            ],
            attributes={
                'a': ['href', 'title'],
                'img': ['src', 'alt', 'title'],
                'code': ['class'],
                'span': ['class'],
                'div': ['class']
            },
            protocols=['http', 'https', 'mailto', 'data']
        )
        html = cleaner.clean(html)
        return html

    def calculate_hash(self):
        import hashlib

        return hashlib.md5(self.content_md.encode('utf-8')).hexdigest()
    class Meta:
        db_table = 'user_profile'
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'
    def __str__(self):
        return f"{self.user_Login.username} - {self.introduction}"

# class Article(models.Model): #一对多关系
#     title = models.CharField(max_length=100)
#     content = models.TextField(max_length=1000)
#
#     # on_delete=models.CASCADE 表示当Article表中的数据被删除时，关联的User_Login表中的数据也会被删除
#     # on_delete=models.SET_NULL 表示当Article表中的数据被删除时，关联的User_Login表中的数据的值设置为null
#     # on_delete=models.PROTECT 表示如果Article表中的数据被删除，则User_Login表中的数据也不能被删除
#     # on_delete=models.DO_NOTHING 表示当Article表中的数据被删除时，关联的User_Login表中的数据的值不进行任何处理
#
#     # related_name='articles' 表示在User_Login表中的articles字段表示关联到Article表的数据
#     author = models.ForeignKey('User_Login',on_delete=models.CASCADE,related_name='articles') #外键关联到User_Login表
#
# class UserExtension(models.Model):
#     birthday = models.DateField(null=True)
#     school = models.CharField(max_length=50,null=True)
#
#     # 一对一关系
#     user = models.OneToOneField('User_Login',on_delete=models.CASCADE,related_name='extension')
#
# class ArticleTag(models.Model):
#     name = models.CharField(max_length=20)
#
#     # 多对多关系
#     articles = models.ManyToManyField('Article',related_name='tags')
#
# class Comment(models.Model):
#     content = models.TextField(max_length=500)
#
#     # 二级评论 外键关联到Comment表
#     original_comment = models.ForeignKey('self',on_delete=models.CASCADE,null=True)
