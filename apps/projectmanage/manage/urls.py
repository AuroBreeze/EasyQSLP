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
    TagProposalDecisionJsonView,
    TagProposalCancelJsonView,
    TagProposalStatusView,
    TagProposalMyHistoryView,
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
    path("tags", TagListView.as_view(), name="tag-list"),  # 
    path("tag-proposals", TagProposalCreateView.as_view(), name="tag-proposal-create"),  # 
    path("tag-proposals/list", TagProposalListView.as_view(), name="tag-proposal-list"),  # 获取标签列表
    path("tag-proposals/decision", TagProposalDecisionJsonView.as_view(), name="tag-proposal-decision-json"),  # 审批标签
    path("tag-proposals/cancel", TagProposalCancelJsonView.as_view(), name="tag-proposal-cancel-json"),  # 取消申请标签
    path("tag-proposals/status", TagProposalStatusView.as_view(), name="tag-proposal-status"),  # 获取标签提案状态
    path("tag-proposals/my-history", TagProposalMyHistoryView.as_view(), name="tag-proposal-my-history"),  # 我的标签申请历史
]