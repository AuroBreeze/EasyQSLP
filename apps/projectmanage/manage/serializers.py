from ..models import Article,Project
from rest_framework import serializers
import markdown
from django.contrib.auth import get_user_model

User = get_user_model()

class ProjectSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=50, required=True)
    cover_image = serializers.ImageField(max_length=None, allow_empty_file=False, allow_null=True, required=False)
    introduction = serializers.CharField(max_length=50, required=False,default='该项目暂未简介')
    maintainers = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)

    class Meta:
        model = Project
        fields = ['id', 'title', 'cover_image', 'introduction', 'status', 'create_time', 'update_time', 'owner',
                  'collaborator', 'replications', 'likes', 'stars', 'short_term_score', 'long_term_score', 'views',
                  'maintainers']
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
        fields = ['id','title', 'content_md', 'content_html', 'toc', 'word_count','create_time','update_time','adminer','project','category']

        extra_kwargs = {
            'content_md': {
                'write_only': True
            }
        }

    def validate(self, attrs):
        # 确保文章必须有项目归属
        if not attrs.get('project') and (self.instance is None or not getattr(self.instance, 'project', None)):
            raise serializers.ValidationError({'project': '文章必须隶属于某个项目'})
        return super().validate(attrs)

    def create(self, validated_data):
        """
        保底设置分类：若未传 category，则自动使用/创建一个名为“默认分类”的分类，避免外键约束失败。
        """
        if not validated_data.get('category'):
            from ..models import Article_category
            category, _ = Article_category.objects.get_or_create(
                name='默认分类'
            )
            validated_data['category'] = category
        return super().create(validated_data)

    def get_toc(self, obj):
        """
        生成目录
        """
        md = markdown.Markdown(extensions=['markdown.extensions.toc'])
        md.convert(obj.content_md)
        return md.toc

    def get_word_count(self, obj):
        return len(obj.content_md.split())


class ArticleRevisionSerializer(serializers.ModelSerializer):
    class Meta:
        from ..models import Article_Revision
        model = Article_Revision
        fields = ['id', 'article', 'content', 'submitter', 'comment', 'status', 'create_time']
        read_only_fields = ['status', 'create_time']


class RevisionApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        from ..models import RevisionApproval
        model = RevisionApproval
        fields = ['id', 'revision', 'approver', 'decision', 'create_time']
        read_only_fields = ['create_time']

    def validate(self, attrs):
        revision = attrs.get('revision')
        approver = attrs.get('approver')
        if not revision or not approver:
            return attrs
        # 只有项目维护者才能审批
        project = revision.article.project
        if not project.maintainers.filter(pk=approver.pk).exists():
            raise serializers.ValidationError({'approver': '只有项目维护者可以进行审批'})
        return attrs


