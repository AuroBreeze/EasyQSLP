from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Article,Article_category,Project, Article_Revision
from apps.user.models import User_Login
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your tests here.



class ProjectTestCase(TestCase):
    def setUp(self):
        self.client: APIClient = APIClient()
        self.projectpost_url = reverse('project:projecttest')
        self.projectget_url = reverse('project:project',kwargs={'pk':1})
        self.user = User_Login.objects.create_user(email='test@example.com', password='testpassword', username='testuser')
        self.client.force_authenticate(user=self.user)

        self.valided_data = {
            'title': 'Test Project',
            'introduction': 'This is a test project.',
            'owner': self.user.id,
            #'creat_time':timezone.now()
            #'id':self.user.id
        }

    def test_create_project(self):
        response = self.client.post(self.projectpost_url, self.valided_data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.get(title='Test Project').title, 'Test Project')
        self.assertEqual(Project.objects.get(title='Test Project').owner, self.user)

    def test_read_project_valid_data(self):
        response = self.client.post(self.projectpost_url, self.valided_data, format='json')
        #print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.get().title, 'Test Project')

class ArticleTestCase(TestCase):
    def setUp(self):
        self.client: APIClient = APIClient()
        self.articlepost_url = reverse('project:articletest')
        self.articleget_url = reverse('project:article',kwargs={'pk':1})
        self.user = User_Login.objects.create_user(email='test@example.com', password='testpassword', username='testuser')

        self.client.force_authenticate(user=self.user)

        self.project = Project.objects.create(title='Test Project', owner=self.user)
        self.category = Article_category.objects.create(name='Test Category')


        self.valided_data = {
            'title': 'Test Article',
            'content_md': "'''This is a test article123.'''",
            'category': self.category.id,
            'project': self.project.id,
            'adminer': self.user.id,
            #'creat_time':timezone.now()
            #'id':self.user.id
        }

    def test_create_article(self):
        response = self.client.post(self.articlepost_url, self.valided_data, format='json')
        #print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.get(title='Test Article').title, 'Test Article')
        self.assertEqual(Article.objects.get(title='Test Article').adminer, self.user)
        self.assertEqual(Article.objects.get(title='Test Article').category, self.category)
        self.assertEqual(Article.objects.get(title='Test Article').project, self.project)

    def test_read_article_valid_data(self):
        response = self.client.post(self.articlepost_url, self.valided_data, format='json')
        #print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.get().title, 'Test Article')

        response = self.client.get(self.articleget_url, format='json')
        #print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_article_must_have_project(self):
        # 不提供 project，应该 400
        invalid = dict(self.valided_data)
        invalid.pop('project', None)
        response = self.client.post(self.articlepost_url, invalid, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('project', response.data)


class RevisionApprovalWorkflowTestCase(TestCase):
    def setUp(self):
        self.client: APIClient = APIClient()
        # 路由
        self.revision_create_url = reverse('project:article-revision-create')
        self.revision_approval_url = reverse('project:revision-approval')

        # 用户
        self.owner = User_Login.objects.create_user(email='owner@example.com', password='pwd', username='owner')
        self.maintainer1 = User_Login.objects.create_user(email='m1@example.com', password='pwd', username='m1')
        self.maintainer2 = User_Login.objects.create_user(email='m2@example.com', password='pwd', username='m2')
        self.maintainer3 = User_Login.objects.create_user(email='m3@example.com', password='pwd', username='m3')
        self.other_user = User_Login.objects.create_user(email='other@example.com', password='pwd', username='other')

        self.client.force_authenticate(user=self.owner)

        # 项目/文章
        self.project = Project.objects.create(title='Workflow Project', owner=self.owner)
        # 设置维护者
        self.project.maintainers.add(self.maintainer1, self.maintainer2, self.maintainer3)

        self.category = Article_category.objects.create(name='Default')
        self.article = Article.objects.create(
            title='Workflow Article',
            content_md='original content',
            adminer=self.owner,
            category=self.category,
            project=self.project,
        )

    def test_approval_requires_maintainer(self):
        # 创建修订
        payload_rev = {
            'article': self.article.id,
            'content': 'new content',
            'submitter': self.owner.id,
            'comment': 'update content',
        }
        r = self.client.post(self.revision_create_url, payload_rev, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        rev_id = r.data['id']

        # 非维护者审批应失败
        self.client.force_authenticate(user=self.other_user)
        payload_app = {
            'revision': rev_id,
            'approver': self.other_user.id,
            'decision': 'approved'
        }
        a = self.client.post(self.revision_approval_url, payload_app, format='json')
        self.assertEqual(a.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('approver', a.data)

    def test_auto_apply_after_three_approvals(self):
        # 创建修订
        payload_rev = {
            'article': self.article.id,
            'content': 'new content v2',
            'submitter': self.owner.id,
            'comment': 'update content v2',
        }
        r = self.client.post(self.revision_create_url, payload_rev, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        rev_id = r.data['id']

        # 先两名维护者同意，不应合入
        for user in [self.maintainer1, self.maintainer2]:
            self.client.force_authenticate(user=user)
            a = self.client.post(self.revision_approval_url, {
                'revision': rev_id,
                'approver': user.id,
                'decision': 'approved'
            }, format='json')
            self.assertEqual(a.status_code, status.HTTP_201_CREATED)

        rev = Article_Revision.objects.get(pk=rev_id)
        rev.refresh_from_db()
        self.assertEqual(rev.status, Article_Revision.Status.PENDING)
        self.article.refresh_from_db()
        self.assertEqual(self.article.content_md, 'original content')

        # 第三名维护者同意，应自动合入
        self.client.force_authenticate(user=self.maintainer3)
        a3 = self.client.post(self.revision_approval_url, {
            'revision': rev_id,
            'approver': self.maintainer3.id,
            'decision': 'approved'
        }, format='json')
        self.assertEqual(a3.status_code, status.HTTP_201_CREATED)

        rev.refresh_from_db()
        self.assertEqual(rev.status, Article_Revision.Status.APPROVED)
        self.article.refresh_from_db()
        self.assertEqual(self.article.content_md, 'new content v2')


class HistoryAndDiffTestCase(TestCase):
    def setUp(self):
        self.client: APIClient = APIClient()

        self.owner = User_Login.objects.create_user(email='owner2@example.com', password='pwd', username='owner2')
        self.m1 = User_Login.objects.create_user(email='m11@example.com', password='pwd', username='m11')
        self.m2 = User_Login.objects.create_user(email='m22@example.com', password='pwd', username='m22')
        self.m3 = User_Login.objects.create_user(email='m33@example.com', password='pwd', username='m33')

        self.client.force_authenticate(user=self.owner)

        self.project = Project.objects.create(title='History Project', owner=self.owner)
        self.project.maintainers.add(self.m1, self.m2, self.m3)

        self.category = Article_category.objects.create(name='HistCat')
        self.article = Article.objects.create(
            title='Hist Article',
            content_md='v0',
            adminer=self.owner,
            category=self.category,
            project=self.project,
        )

        # urls
        self.rev_create_url = reverse('project:article-revision-create')
        self.rev_list_url = reverse('project:article-revision-list', kwargs={'pk': self.article.id})

    def _approve(self, rev_id, approver):
        url = reverse('project:revision-approval')
        self.client.force_authenticate(user=approver)
        return self.client.post(url, {
            'revision': rev_id,
            'approver': approver.id,
            'decision': 'approved'
        }, format='json')

    def test_revision_list_and_diff(self):
        # 创建两个修订
        r1 = self.client.post(self.rev_create_url, {
            'article': self.article.id,
            'content': 'v1',
            'submitter': self.owner.id,
            'comment': 'to v1',
        }, format='json')
        self.assertEqual(r1.status_code, status.HTTP_201_CREATED)
        rev1_id = r1.data['id']

        # 审批合入 r1
        for u in [self.m1, self.m2, self.m3]:
            a = self._approve(rev1_id, u)
            self.assertEqual(a.status_code, status.HTTP_201_CREATED)

        # 再创建 r2
        r2 = self.client.post(self.rev_create_url, {
            'article': self.article.id,
            'content': 'v2',
            'submitter': self.owner.id,
            'comment': 'to v2',
        }, format='json')
        self.assertEqual(r2.status_code, status.HTTP_201_CREATED)
        rev2_id = r2.data['id']

        # 列表应至少包含 r1 和 r2
        lst = self.client.get(self.rev_list_url)
        self.assertEqual(lst.status_code, status.HTTP_200_OK)
        ids = [item['id'] for item in lst.data]
        self.assertIn(rev1_id, ids)
        self.assertIn(rev2_id, ids)

        # 查看 r2 与 prev 的 diff
        diff_url_prev = reverse('project:revision-diff', kwargs={'pk': rev2_id}) + '?against=prev&mode=unified'
        dprev = self.client.get(diff_url_prev)
        self.assertEqual(dprev.status_code, status.HTTP_200_OK)
        self.assertIn('diff', dprev.data)

        # 查看 r2 与 current 的 diff（current 仍是 v1，因为 r2 未合入）
        diff_url_cur = reverse('project:revision-diff', kwargs={'pk': rev2_id}) + '?against=current&mode=unified'
        dcur = self.client.get(diff_url_cur)
        self.assertEqual(dcur.status_code, status.HTTP_200_OK)
        self.assertIn('diff', dcur.data)

    def test_revert_flow(self):
        # 创建并合入 r1(v1)
        r1 = self.client.post(self.rev_create_url, {
            'article': self.article.id,
            'content': 'v1',
            'submitter': self.owner.id,
            'comment': 'to v1',
        }, format='json')
        rev1_id = r1.data['id']
        for u in [self.m1, self.m2, self.m3]:
            a = self._approve(rev1_id, u)
            self.assertEqual(a.status_code, status.HTTP_201_CREATED)

        # 创建并合入 r2(v2)
        r2 = self.client.post(self.rev_create_url, {
            'article': self.article.id,
            'content': 'v2',
            'submitter': self.owner.id,
            'comment': 'to v2',
        }, format='json')
        rev2_id = r2.data['id']
        for u in [self.m1, self.m2, self.m3]:
            a = self._approve(rev2_id, u)
            self.assertEqual(a.status_code, status.HTTP_201_CREATED)

        # 现在文章应为 v2
        self.article.refresh_from_db()
        self.assertEqual(self.article.content_md, 'v2')

        # 维护者发起回滚到 r1
        self.client.force_authenticate(user=self.m1)
        revert_url = reverse('project:revision-revert', kwargs={'pk': rev1_id})
        rv = self.client.post(revert_url)
        self.assertEqual(rv.status_code, status.HTTP_201_CREATED)
        revert_id = rv.data['id']

        # 审批回滚修订
        for u in [self.m1, self.m2, self.m3]:
            a = self._approve(revert_id, u)
            self.assertEqual(a.status_code, status.HTTP_201_CREATED)

        # 回滚合入后应变回 v1
        self.article.refresh_from_db()
        self.assertEqual(self.article.content_md, 'v1')


