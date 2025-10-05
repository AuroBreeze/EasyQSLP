from django.contrib import admin
from .models import Article_tag, TagProposal


@admin.register(Article_tag)
class ArticleTagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(TagProposal)
class TagProposalAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "status", "submitter", "approved_by", "approved_time", "create_time")
    list_filter = ("status",)
    search_fields = ("name", "submitter__username", "approved_by__username")
