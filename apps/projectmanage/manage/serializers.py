from ..models import Article,Project
from rest_framework import serializers
import markdown

class ProjectSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=50, required=True)
    cover_image = serializers.ImageField(max_length=None, allow_empty_file=False, allow_null=True, required=False)
    introduction = serializers.CharField(max_length=50, required=False,default='该项目暂未简介')

    class Meta:
        model = Project
        fields = ['title', 'cover_image', 'introduction', 'status', 'create_time', 'update_time', 'owner',
                  'collaborator', 'replications', 'likes', 'stars', 'short_term_score', 'long_term_score', 'views']
        extra_kwargs = {
            'collaborator': {
                'read_only': True,
            },'replications': {
                'read_only': True,
            },'likes': {
                'read_only': True,
            },'stars': {
                'read_only': True,
            }
        }


class ArticleSerializer(serializers.ModelSerializer):
    toc = serializers.SerializerMethodField()
    word_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['title', 'content_md', 'content_html', 'toc', 'word_count','create_time','update_time','adminer','project']

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


