from .serializers import ArticleSerializer
from ..models import Article
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView

class ArticleView(APIView):
    def get(self,request):
        articles = Article.objects.all()
    def post(self,requests):
        serializer = ArticleSerializer(data=requests.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)

