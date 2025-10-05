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
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.projectmanage.services.diff import DiffService
from apps.utils.auth.permissions import IsOperatorOrSuperuser
from django.db import transaction
from django.utils import timezone
from apps.utils.errors.ErrorExtract import ExtractError


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
        # 统一错误响应格式，不暴露具体字段名（如 tags_ids）
        errors = ExtractError(serializer.errors).extract_error()
        # 若包含标签相关错误，汇总为统一提示
        if 'tags_ids' in errors:
            unified_msg = '所选标签不存在或未通过'
        else:
            # 合并所有错误到一个 ValidationError 提示
            msg_list = []
            if isinstance(errors, dict):
                for v in errors.values():
                    if isinstance(v, (list, tuple)):
                        msg_list.extend([str(x) for x in v if x is not None])
                    elif v is not None:
                        msg_list.append(str(v))
            unified_msg = '；'.join(msg_list) if msg_list else '参数错误'
        return Response({
            "success": False,
            "message": "Invalid data",
            "errors": {"ValidationError": unified_msg}
        }, status=400)


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
        # 返回全部标签（移除 q 模糊搜索）
        qs = Article_tag.objects.all().order_by('name')
        items = TagMiniSerializer(qs, many=True).data
        return Response({
            "success": True,
            "message": "查询成功",
            "data": items
        })


class TagProposalCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        from .serializers import TagProposalCreateSerializer, TagProposalSerializer
        from ..models import TagProposal, Article_tag
        serializer = TagProposalCreateSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            # 幂等：若已存在同名待审申请，直接返回该申请
            existed = TagProposal.objects.filter(name=name, status=TagProposal.Status.PENDING).order_by('-create_time').first()
            if existed:
                return Response({
                    "success": True,
                    "message": "已存在同名待审核申请",
                    "data": TagProposalSerializer(existed).data
                }, status=status.HTTP_200_OK)
            # 若标签已存在（全站复用），不再创建申请
            if Article_tag.objects.filter(name=name).exists():
                return Response({
                    "success": False,
                    "message": "Invalid data",
                    "errors": {"ValidationError": "标签已存在，无需申请"}
                }, status=status.HTTP_400_BAD_REQUEST)
            proposal = serializer.save()
            return Response({
                "success": True,
                "message": "提交成功，等待审核",
                "data": TagProposalSerializer(proposal).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "success": False,
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class TagProposalListView(APIView):
    permission_classes = [IsAuthenticated, IsOperatorOrSuperuser]

    def post(self, request, *args, **kwargs):
        from .serializers import TagProposalSerializer
        from ..models import TagProposal
        # status 为必填
        status_filter = request.data.get('status')
        if not status_filter:
            return Response({
                "success": False,
                "message": "Invalid data",
                "errors": {"ValidationError": "status 为必填"}
            }, status=status.HTTP_400_BAD_REQUEST)

        # 校验合法取值
        valid_status = {c[0] for c in TagProposal.Status.choices}
        if status_filter not in valid_status:
            return Response({
                "success": False,
                "message": "Invalid data",
                "errors": {"ValidationError": "status 取值无效"}
            }, status=status.HTTP_400_BAD_REQUEST)

        qs = TagProposal.objects.filter(status=status_filter).order_by('-create_time')

        # 分页参数：page, page_size
        try:
            page = int(request.data.get('page', 1))
            page_size = int(request.data.get('page_size', 10))
        except Exception:
            return Response({
                "success": False,
                "message": "Invalid data",
                "errors": {"ValidationError": "分页参数必须为数字"}
            }, status=status.HTTP_400_BAD_REQUEST)

        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 10
        # 限制最大分页大小，避免一次性返回过多
        if page_size > 100:
            page_size = 100

        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_qs = qs[start:end]
        items = TagProposalSerializer(page_qs, many=True).data

        return Response({
            "success": True,
            "message": "查询成功",
            "data": {
                "total": total,
                "page": page,
                "page_size": page_size,
                "item": items
            }
        })


class TagProposalDecisionJsonView(APIView):
    permission_classes = [IsAuthenticated, IsOperatorOrSuperuser]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        from .serializers import TagProposalDecisionSerializer, TagProposalSerializer
        from ..models import TagProposal, Article_tag

        proposal_id = request.data.get('id')
        if not proposal_id:
            return Response({
                "success": False,
                "message": "Invalid data",
                "errors": {"ValidationError": "id 为必填"}
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            proposal = TagProposal.objects.select_for_update().get(pk=proposal_id)
        except TagProposal.DoesNotExist:
            return Response({
                "success": False,
                "message": "Not found",
                "errors": {"ValidationError": "申请不存在"}
            }, status=status.HTTP_404_NOT_FOUND)

        if proposal.status != TagProposal.Status.PENDING:
            return Response({
                "success": False,
                "message": "Invalid data",
                "errors": {"ValidationError": "该申请已处理"}
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = TagProposalDecisionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Invalid data",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        decision = serializer.validated_data['decision']
        comment = serializer.validated_data.get('comment', '')

        if decision == 'approved':
            # 复用或创建全局唯一标签
            tag, _ = Article_tag.objects.get_or_create(name=proposal.name)
            proposal.final_tag = tag
            proposal.status = TagProposal.Status.APPROVED
            proposal.approved_by = request.user
            proposal.approved_time = timezone.now()
            proposal.comment = comment or proposal.comment
            proposal.save(update_fields=['final_tag', 'status', 'approved_by', 'approved_time', 'comment', 'update_time'])
            return Response({
                "success": True,
                "message": "已通过",
                "data": TagProposalSerializer(proposal).data
            })
        else:
            proposal.status = TagProposal.Status.REJECTED
            proposal.approved_by = request.user
            proposal.approved_time = timezone.now()
            proposal.comment = comment or proposal.comment
            proposal.save(update_fields=['status', 'approved_by', 'approved_time', 'comment', 'update_time'])
            return Response({
                "success": True,
                "message": "已拒绝",
                "data": TagProposalSerializer(proposal).data
            })


class TagProposalCancelJsonView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        from .serializers import TagProposalSerializer
        from ..models import TagProposal
        proposal_id = request.data.get('id')
        if not proposal_id:
            return Response({
                "success": False,
                "message": "Invalid data",
                "errors": {"ValidationError": "id 为必填"}
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            proposal = TagProposal.objects.select_for_update().get(pk=proposal_id)
        except TagProposal.DoesNotExist:
            return Response({
                "success": False,
                "message": "Not found",
                "errors": {"ValidationError": "申请不存在"}
            }, status=status.HTTP_404_NOT_FOUND)

        # 权限：提交者本人或运营/超管
        user = request.user
        is_operator = getattr(user, 'is_superuser', False) or user.groups.filter(name='Operator').exists()
        if not (proposal.submitter_id == getattr(user, 'id', None) or is_operator):
            return Response({
                "success": False,
                "message": "Forbidden",
                "errors": {"ValidationError": "无权限取消该申请"}
            }, status=status.HTTP_403_FORBIDDEN)

        if proposal.status != TagProposal.Status.PENDING:
            return Response({
                "success": False,
                "message": "Invalid data",
                "errors": {"ValidationError": "仅待审核申请可取消"}
            }, status=status.HTTP_400_BAD_REQUEST)

        comment = request.data.get('comment')
        if comment:
            proposal.comment = comment
        proposal.status = TagProposal.Status.CANCELED
        proposal.save(update_fields=['status', 'comment', 'update_time'])

        return Response({
            "success": True,
            "message": "已取消",
            "data": TagProposalSerializer(proposal).data
        })
