from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Project(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft','草稿'
        PUBLISHED = 'published','已发布'
        UNDER_REVIEW = 'under_review','审核中'

    title = models.CharField(max_length=50,unique=True,verbose_name='项目名称')
    owner = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='projects',verbose_name='项目管理者')
    collaborator = models.ManyToManyField(User,related_name='collaborated_projects',verbose_name='项目协作者')
    version = models.OneToOneField("ProjectVersion",on_delete=models.SET_NULL,null=True,blank=True,related_name='project_versions',verbose_name='项目版本')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    cover_image = models.ImageField(upload_to='project_cover_image',verbose_name='项目封面图')

    class Meta:
        db_table = "project"
        verbose_name = '项目'
        verbose_name_plural = '项目'


class ProjectVersion(models.Model):
    pass

class Article_category(models.Model):
    name = models.CharField(max_length=50,verbose_name='分类名称')
    def __str__(self):
        return self.name
    class Meta:
        db_table = "project_article_category"
        verbose_name = '文章分类'
        verbose_name_plural = '文章分类'

# Create your models here.
class Article(models.Model):
    title = models.TextField(max_length=50,verbose_name='项目名称')

    adminer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles',
                                verbose_name='文章管理者')
    category = models.ForeignKey('Article_category', on_delete=models.SET_DEFAULT, default=1,
                                 related_name='articles', verbose_name='文章分类')

    introdect = models.TextField(max_length=200,verbose_name='项目简介',default='暂无简介')
    content_md = models.TextField(verbose_name='项目内容markdown') #存储原始markdown
    content_html = models.TextField(verbose_name='项目内容html') #存储渲染后的html
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    def __str__(self):
        return f"文章管理者{self.adminer.username}，文章标题{self.title}"
    class Meta:
        db_table = "project_article"
        verbose_name = '项目文章'
        verbose_name_plural = '项目文章'

class Article_comment(models.Model):
    article = models.ForeignKey('Article',on_delete=models.CASCADE,related_name='comments',verbose_name='文章')
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='comments',verbose_name='评论者')


    content = models.TextField(max_length=200,verbose_name='评论内容')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='评论时间')
    def __str__(self):
        return f"文章{self.article.title}，评论者{self.user.username}，评论内容{self.content}"
    class Meta:
        db_table = "project_article_comment"
        verbose_name = '文章评论'
        verbose_name_plural = '文章评论'
    
    