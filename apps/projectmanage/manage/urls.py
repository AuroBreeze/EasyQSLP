from django.urls import path
from .views import (
    ArticleView,
    ProjectView,
    ArticleRevisionView,
    RevisionApprovalView,
    ArticleRevisionListView,
    RevisionDiffView,
    RevisionRevertView,
    TagListView,
    TagProposalCreateView,
    TagProposalListView,
    TagProposalDecisionView,
)

app_name = 'project'
urlpatterns = [
    path("articletest",ArticleView.as_view(),name="articletest"),
    path("article/<int:pk>/",ArticleView.as_view(),name="article"),
    path("article/<int:pk>/revisions", ArticleRevisionListView.as_view(), name="article-revision-list"),
    path("project/<int:pk>/",ProjectView.as_view(),name="project"),
    path("project",ProjectView.as_view(),name="projecttest"),
    path("revision/<int:pk>/", ArticleRevisionView.as_view(), name="article-revision-detail"),
    path("revision", ArticleRevisionView.as_view(), name="article-revision-create"),
    path("revision/approval", RevisionApprovalView.as_view(), name="revision-approval"),
    path("revision/<int:pk>/diff", RevisionDiffView.as_view(), name="revision-diff"),
    path("revision/<int:pk>/revert", RevisionRevertView.as_view(), name="revision-revert"),
    path("tags", TagListView.as_view(), name="tag-list"),
    path("tag-proposals", TagProposalCreateView.as_view(), name="tag-proposal-create"),
    path("tag-proposals/list", TagProposalListView.as_view(), name="tag-proposal-list"),
    path("tag-proposals/<int:pk>/decision", TagProposalDecisionView.as_view(), name="tag-proposal-decision"),
]