from ..models import Article
from rest_framework import serializers
import markdown

class ArticleSerializer(serializers.ModelSerializer):
    toc = serializers.SerializerMethodField()
    word_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'content_md', 'content_html', 'toc', 'word_count','update_time']

        extra_kwargs = {
            'content_md': {
                'write_only': True
            }
        }

    def get_toc(self, obj):
        """
        生成目录
        """
        md = markdown.Markdown(extensions=['markdown.extensions.toc'])
        md.convert(obj.content_md)
        return md.toc

    def get_word_count(self, obj):
        return len(obj.content_md.split())


