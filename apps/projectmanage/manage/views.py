from rest_framework.generics import get_object_or_404

from .serializers import ArticleSerializer,ProjectSerializer
from ..models import Article,Project
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView


class ProjectView(APIView):
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


