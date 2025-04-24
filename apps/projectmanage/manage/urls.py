from django.urls import path
from .views import *

app_name = 'project'
urlpatterns = [
    path("articletest",ArticleDetailView.as_view(),name="articletest")
]