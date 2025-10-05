from django.contrib import admin
from .models import Article_tag


@admin.register(Article_tag)
class ArticleTagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
