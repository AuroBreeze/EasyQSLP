from django.db import models
from apps.users.models import User_Login
# Create your models here.
class Article(models.Model):
    adminer = models.ForeignKey(User_Login, on_delete=models.SET_NULL, null=True,blank=True)
    title = models.TextField(min_length=1,max_length=50,verbose_name=' 项目名称')
    introdect = models.TextField(max_length=200,verbose_name=' 项目简介',default='暂无简介')
    content_md = models.TextField(verbose_name=' 项目内容markdown') #存储原始markdown
    content_html = models.TextField(verbose_name=' 项目内容html') #存储渲染后的html
    create_time = models.DateTimeField(auto_now_add=True,verbose_name=' 创建时间')
    update_time = models.DateTimeField(auto_now=True,verbose_name=' 更新时间')
    def __str__(self):
        return f"文章管理者{self.adminer.username}，文章标题{self.title}"
    class Meta:
        verbose_name = '项目文章'
        verbose_name_plural = ' 项目文章'
    
    
    