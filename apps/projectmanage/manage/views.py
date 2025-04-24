from .serializers import ArticleSerializer
from ..models import Article
from rest_framework import generics
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView

class ArticleViewMixin(generics.GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_queryset(self):
        return super().get_queryset().select_related('project', 'category', 'adminer')

class ArticleDetailView(ArticleViewMixin,generics.RetrieveUpdateDestroyAPIView):
    def retrieve(self, request, *args, **kwargs):
        cache_key = f'article_{kwargs["pk"]}_html'
        cached_html = cache.get(cache_key)

        if cached_html:
            return Response({'html': cached_html})

        instance = self.get_object()
        serializer = self.get_serializer(instance)

        cache.set(cache_key, serializer.data['content_html'], 60 * 60 * 12)
        return Response(serializer.data)

