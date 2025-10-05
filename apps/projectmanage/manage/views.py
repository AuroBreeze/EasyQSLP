from rest_framework.generics import get_object_or_404
from .serializers import (
    ArticleSerializer,
    ProjectSerializer,
    ArticleRevisionSerializer,
    RevisionApprovalSerializer,
    TagMiniSerializer,
)
from ..models import Article, Project, Article_Revision, Article_tag
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from apps.projectmanage.services.diff import DiffService


class ProjectView(APIView):
    def get_permissions(self):
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
            # 记录合入执行者（最后一次审批人），便于审计
            revision.applied_by = getattr(request, 'user', None)
            if revision.applied_by_id:
                revision.save(update_fields=['applied_by'])
            revision.apply_if_ready()
            return Response(RevisionApprovalSerializer(approval).data, status=201)
        return Response(serializer.errors, status=400)


class ArticleRevisionListView(APIView):
    def get_permissions(self):
        return [AllowAny()]

    def get(self, request, *args, **kwargs):
        article_id = kwargs.get('pk')
        article = get_object_or_404(Article, pk=article_id)
        qs = Article_Revision.objects.filter(article=article).order_by('-version', '-create_time')
        data = ArticleRevisionSerializer(qs, many=True).data
        return Response(data)


class RevisionDiffView(APIView):
    def get_permissions(self):
        return [AllowAny()]

    def get(self, request, *args, **kwargs):
        rev_id = kwargs.get('pk')
        revision = get_object_or_404(Article_Revision, pk=rev_id)
        against = request.query_params.get('against', 'prev')  # prev|current
        mode = request.query_params.get('mode', 'unified')  # unified|html|dmp
        if against == 'current':
            old = revision.article.content_md or ''
        else:
            old = (revision.parent.content if revision.parent else '')
        new = revision.content
        diff = DiffService(mode=mode).diff(old, new)
        return Response({'revision': revision.id, 'against': against, 'mode': mode, 'diff': diff})


class RevisionRevertView(APIView):
    def get_permissions(self):
        return [AllowAny()]

    def post(self, request, *args, **kwargs):
        rev_id = kwargs.get('pk')
        revision = get_object_or_404(Article_Revision, pk=rev_id)
        project = revision.article.project
        user = getattr(request, 'user', None)
        # 仅维护者可以发起回滚
        if not user or not project.maintainers.filter(pk=getattr(user, 'pk', None)).exists():
            return Response({'detail': '只有项目维护者可以回滚'}, status=403)

        # 以当前文章为基线，创建一个新的修订，内容回滚到目标修订
        article = revision.article
        new_content = revision.content

        import hashlib
        base_hash = hashlib.md5((article.content_md or '').encode('utf-8')).hexdigest()

        parent = (
            Article_Revision.objects.filter(article=article, status=Article_Revision.Status.APPROVED)
            .order_by('-version')
            .first()
        )

        # 生成 diff
        diff = DiffService(mode='unified').diff(article.content_md or '', new_content)

        revert_rev = Article_Revision.objects.create(
            article=article,
            content=new_content,
            submitter=user,
            comment=f'Revert to revision {revision.id}',
            parent=parent,
            base_content_hash=base_hash,
            diff_json=diff,
        )

        return Response(ArticleRevisionSerializer(revert_rev).data, status=201)


class TagListView(APIView):
    def get_permissions(self):
        return [AllowAny()]

    # 使用 JSON + POST 的方式获取/搜索标签
    def post(self, request, *args, **kwargs):
        q = request.data.get('q')
        qs = Article_tag.objects.all().order_by('name')
        if q:
            qs = qs.filter(name__icontains=q)
        items = TagMiniSerializer(qs, many=True).data
        return Response({
            "success": True,
            "message": "查询成功",
            "data": items
        })

