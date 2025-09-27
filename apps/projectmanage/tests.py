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


