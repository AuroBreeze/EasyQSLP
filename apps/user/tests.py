from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User_Login, Email_Verify_Code
from django.utils import timezone


class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('user:register')
        self.valid_payload = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpassword',
            'code': '123456',
            'usage': 'Register'
        }
        # 创建一个验证码
        Email_Verify_Code.objects.update_or_create(
            email='test@example.com',
            defaults={
                'code': '123456'
                'send_time': timezone.now(),
                'expire_time': timezone.now() + timezone.timedelta(minutes=5),
                'usage': 'Register'
            }
        )

    def test_valid_user_registration(self):
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User_Login.objects.filter(email='test@example.com').exists())

    def test_invalid_user_registration(self):
        # 测试无效的验证码
        invalid_payload = self.valid_payload.copy()
        invalid_payload['code'] = '654321'
        response = self.client.post(self.register_url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UserLoginTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('user:login')
        self.user = User_Login.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpassword',
            is_active=True
        )

    def test_valid_user_login(self):
        valid_payload = {
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.login_url, valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_user_login(self):
        invalid_payload = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)