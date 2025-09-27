from rest_framework.generics import get_object_or_404

from .serializers import (
    ArticleSerializer,
    ProjectSerializer,
    ArticleRevisionSerializer,
    RevisionApprovalSerializer,
)
from ..models import Article, Project, Article_Revision
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny


class ProjectView(APIView):
    def get_permissions(self):
        """TODO: 测试阶段：全部放开权限（GET/POST 均无需登录）。上线请恢复。"""
        return [AllowAny()]

    def get(self,request,*args,**kwargs):
        project_id = kwargs.get('pk')
        project = get_object_or_404(Project,pk=project_id)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def post(self,requests):
        serializer = ProjectSerializer(data=requests.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)

class ArticleView(APIView):
    def get_permissions(self):
        """测试阶段：全部放开权限（GET/POST 均无需登录）。上线请恢复。"""
        return [AllowAny()]

    def get(self,request,*args,**kwargs):
        article_id = kwargs.get('pk')
        #print(article_id)
        article = get_object_or_404(Article,pk=article_id)
        #print(article)
        serializer = ArticleSerializer(article)
        #print(serializer.data)
        return Response(serializer.data)

    def post(self,requests):
        serializer = ArticleSerializer(data=requests.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)


class ArticleRevisionView(APIView):
    def get_permissions(self):
        return [AllowAny()]

    def get(self, request, *args, **kwargs):
        rev_id = kwargs.get('pk')
        revision = get_object_or_404(Article_Revision, pk=rev_id)
        serializer = ArticleRevisionSerializer(revision)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ArticleRevisionSerializer(data=request.data)
        if serializer.is_valid():
            revision = serializer.save()
            return Response(ArticleRevisionSerializer(revision).data, status=201)
        return Response(serializer.errors, status=400)


class RevisionApprovalView(APIView):
    def get_permissions(self):
        return [AllowAny()]

    def post(self, request, *args, **kwargs):
        serializer = RevisionApprovalSerializer(data=request.data)
        if serializer.is_valid():
            approval = serializer.save()
            # 审批后尝试自动合入
            revision = approval.revision
            revision.apply_if_ready()
            return Response(RevisionApprovalSerializer(approval).data, status=201)
        return Response(serializer.errors, status=400)


