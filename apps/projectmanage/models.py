from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.html import strip_tags
import math
User = get_user_model()

class Project(models.Model):
    class Status(models.TextChoices):
        PUBLISHED = 'published', '已发布'
        #未发布
        UNPUBLISHED = 'unpublished', '未发布'
        #下架
        SUSPENDED = 'suspended', '下架'
        #删除
        DELETED = 'deleted', '删除'
        

    title = models.CharField(max_length=50,unique=True,verbose_name='项目名称')
    owner = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='projects',verbose_name='项目管理者')
    collaborator = models.ManyToManyField(User,related_name='collaborated_projects',verbose_name='项目协作者')
    # version = models.OneToOneField("ProjectVersion",on_delete=models.SET_NULL,null=True,blank=True,related_name='project_versions',verbose_name='项目版本')
    introduction = models.TextField(max_length=50,default="暂无介绍",verbose_name='项目简介')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    cover_image = models.ImageField(upload_to='project_cover_image',verbose_name='项目封面图')
    
    likes = models.ManyToManyField(User,related_name='liked_projects',verbose_name='喜欢的用户')
    stars = models.ManyToManyField(User,related_name='collected_projects',verbose_name='收藏的用户')
    views = models.IntegerField(default=0,verbose_name='浏览量')
    replications = models.ManyToManyField(User,related_name='replicated_projects',verbose_name='复现的用户')

    hot_score = models.FloatField(default=0.0,verbose_name='热度分数')
    short_term_score = models.FloatField(default=0.0,verbose_name='短期热度分数')
    long_term_score = models.FloatField(default=0.0,verbose_name='长期热度分数')

    status = models.CharField(max_length=20,choices=Status.choices,default=Status.UNPUBLISHED,verbose_name='项目状态')

    class Meta:
        db_table = "project"
        verbose_name = '项目'
        verbose_name_plural = '项目'
        
    def __str__(self):
        return f"项目管理者{self.owner.username}，项目名称{self.title}，"

    def calculate_hot_score(self):
        time_diff = timezone.now() - self.create_time
        hours = time_diff.total_seconds() / 3600

        # 权重设定
        view_weight = 0.1
        like_weight = 1
        star_weight = 2
        replication_weight = 4

        base_score = (
                self.views * view_weight +
                self.likes.count() * like_weight +
                self.stars.count() * star_weight +
                self.replications.count() * replication_weight
        )

        # 时间衰减因子
        gravity_short = 1.8
        gravity_long = 1.1

        # 热度计算
        self.hot_score = base_score / math.pow((hours + 2), gravity_short)
        self.short_term_score = self.hot_score
        self.long_term_score = base_score / math.pow((hours + 2), gravity_long)

        self.save(update_fields=['hot_score', 'short_term_score', 'long_term_score'])

        return {
            "hot_score": self.hot_score,
            "short_term_score": self.short_term_score,
            "long_term_score": self.long_term_score,
        }
# class ProjectVersion(models.Model):
#     pass
#
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
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='articles', verbose_name='所属项目')
    title = models.CharField(max_length=50,verbose_name='文章标题')

    adminer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles',
                                verbose_name='文章管理者')
    category = models.ForeignKey('Article_category', on_delete=models.SET_DEFAULT, default=1,
                                 related_name='articles', verbose_name='文章分类')

    content_md = models.TextField(verbose_name='项目内容markdown') #存储原始markdown
    content_html = models.TextField(editable=False)  # 自动生成的 HTML #存储渲染后的html
    content_hash = models.CharField(max_length=32, editable=False)  # 用于缓存校验
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    def __str__(self):
        return f"文章管理者{self.adminer.username}，文章标题{self.title}"
    class Meta:
        db_table = "project_article"
        verbose_name = '项目文章'
        verbose_name_plural = '项目文章'

    def save(self, *args, **kwargs):
        if not self.content_hash or self.has_content_changed():
            self.html_content = self.generate_safe_html()
            self.content_hash = self.calculate_hash()
        super().save(*args, **kwargs)

    def has_content_changed(self):
        if not self.pk:
            return True
        old = Article.objects.get(pk=self.pk)
        return self.content_md != old.content_md

    def generate_safe_html(self):
        from markdown import markdown
        from bleach.sanitizer import Cleaner

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
        return cleaner.clean(html)

    def calculate_hash(self):
        import hashlib
        return hashlib.md5(self.content_md.encode('utf-8')).hexdigest()
class Article_Revision(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', '待审核'
        APPROVED = 'approved', '已通过'
        REJECTED = 'rejected', '已拒绝'
        CANCELED = 'canceled', '已取消'
    article = models.ForeignKey('Article',on_delete=models.CASCADE,related_name='revisions',verbose_name='文章')
    content = models.TextField(verbose_name='文章内容')
    submitter = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='revision_submitters',verbose_name='提交者')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='提交时间')

    comment = models.TextField(max_length=200,verbose_name='修改说明')
    status = models.CharField(max_length=10,choices=Status.choices,default=Status.PENDING,verbose_name='审核状态')
    def __str__(self):
        return f"文章{self.article.title}，提交者{self.submitter.username}，提交时间{self.create_time}"

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
    
    