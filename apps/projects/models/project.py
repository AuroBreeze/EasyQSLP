from django.db import models
from apps.users.models import CustomUser

class Project(models.Model):
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('published', '已发布'),
        ('archived', '归档'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    repository_url = models.URLField(blank=True)
    documentation = models.FileField(upload_to='projects/docs/')
    
    def __str__(self):
        return self.title