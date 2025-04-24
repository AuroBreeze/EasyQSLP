from django.urls import path
from .views import *

app_name = 'project'
urlpatterns = [
    path("articletest",ArticleView.as_view(),name="articletest"),
    path("article/<int:pk>/",ArticleView.as_view(),name="article"),
    path("project/<int:pk>/",ProjectView.as_view(),name="project"),
    path("project",ProjectView.as_view(),name="projecttest")
]