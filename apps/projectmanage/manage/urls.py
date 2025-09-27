from django.urls import path
from .views import (
    ArticleView,
    ProjectView,
    ArticleRevisionView,
    RevisionApprovalView,
)

app_name = 'project'
urlpatterns = [
    path("articletest",ArticleView.as_view(),name="articletest"),
    path("article/<int:pk>/",ArticleView.as_view(),name="article"),
    path("project/<int:pk>/",ProjectView.as_view(),name="project"),
    path("project",ProjectView.as_view(),name="projecttest"),
    path("revision/<int:pk>/", ArticleRevisionView.as_view(), name="article-revision-detail"),
    path("revision", ArticleRevisionView.as_view(), name="article-revision-create"),
    path("revision/approval", RevisionApprovalView.as_view(), name="revision-approval"),
]