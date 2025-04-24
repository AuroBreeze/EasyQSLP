from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Article,Article_category,Project
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


