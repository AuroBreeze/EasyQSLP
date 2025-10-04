from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(User_Login)
class User_LoginAdmin(admin.ModelAdmin):
    list_display = ('email', 'username','join_date', 'last_login','is_active', 'is_staff', 'is_superuser') # 显示字段
    list_filter = ('is_active', 'is_staff', 'is_superuser') # 过滤器
    list_editable = ('is_active', 'is_staff', 'is_superuser') # 可编辑字段


    search_fields = ('email', 'username','is_active','is_staff', 'is_superuser') # 搜索字段

    ordering = ('email',) # 排序字段
    readonly_fields = ('join_date', 'last_login') # 只读字段
    list_per_page = 15 # 每页显示条数

@admin.register(User_Profile)
class User_ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_Login','userprofile_md') # 显示字段
    list_filter = ('user_Login',) # 过滤器
    search_fields = ('user_Login','userprofile_md') # 搜索字段
    ordering = ('user_Login',) # 排序字段
    
    list_per_page = 15 # 每页显示条数
