from http.client import responses

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User_Login, Email_Verify_Code,User_Profile
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
                'code': '123456',
                'send_time': timezone.now(),
                'expire_time': timezone.now() + timezone.timedelta(minutes=5),
                'usage': 'Register'
            }
        )

    def test_valid_user_registration(self):
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User_Login.objects.get(email='test@example.com')
        self.assertTrue(user.DoesNotExist) # 测试是否创建了用户
        self.assertFalse(user.is_superuser) # 测试是否创建了管理员权限
        self.assertFalse(user.is_staff) # 测试是否创建了管理员权限
        self.assertTrue(User_Profile.objects.filter(user_Login=User_Login.objects.get(email='test@example.com').id)) # 测试是否创建了用户个人资料

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
        self.jwt_token_url = reverse('user:token')
        self.jwt_token_refresh_url = reverse('user:token_refresh')
        self.jwt_token_verify_url = reverse('user:token_verify')
        self.user = User_Login.objects.create_user(email='test@example.com', username='testuser',
                                                   password='testpassword')

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

    def test_valid_jwt_token(self):
        valid_payload = {
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.jwt_token_url, valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.json())
        self.assertIn('refresh', response.json())

        response_refresh_vaile = self.client.post(self.jwt_token_refresh_url, {'refresh': response.json()['refresh']}, format='json')
        self.assertEqual(response_refresh_vaile.status_code, status.HTTP_200_OK)
        self.assertIn('access', response_refresh_vaile.json())
        self.assertIn('refresh', response_refresh_vaile.json())

        response_verify_vaile = self.client.post(self.jwt_token_verify_url, {'token': response.json()['access']}, format='json')
        self.assertEqual(response_verify_vaile.status_code, status.HTTP_200_OK)
        self.assertNotIn('error',response_verify_vaile.json())

    def test_invalid_jwt_token(self):
        invalid_payload = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.jwt_token_url, invalid_payload, format='json')
        #print(response.json())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access', response.json())
        self.assertNotIn('refresh', response.json())

    def test_invalid_jwt_token_verify(self):
        invalid_payload = {
            'token': 'testtoken'
        }
        response = self.client.post(self.jwt_token_verify_url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail',response.json())
        self.assertIn('code',response.json())

    def test_invalid_jwt_token_refresh(self):
        invalid_payload = {
            'refresh': 'testtoken'
        }
        response = self.client.post(self.jwt_token_refresh_url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        #print(response.json())
        self.assertIn('detail', response.json())
        self.assertIn('code', response.json())



class UserResetPasswordTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.reset_pwd_url = reverse('user:restpassword')
        self.user = User_Login.objects.create_user(email='test@example.com', username='testuser',
                                                   password='testpassword')
        self.valid_payload = {
            'email': 'test@example.com',
            'password': 'testpassword123',
            'password_confirm': 'testpassword123',
            'code': '123456',
            'usage': 'ResetPassword'
        }
        # 创建一个验证码
        Email_Verify_Code.objects.update_or_create(
            email='test@example.com',
            defaults={
                'code': '123456',
                'send_time': timezone.now(),
                'expire_time': timezone.now() + timezone.timedelta(minutes=5),
                'usage': 'ResetPassword'
            }
        )
    def test_valid_user_reset_password(self):
        response = self.client.post(self.reset_pwd_url,self.valid_payload,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_user_reset_password(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload['code'] = '654321'
        response = self.client.post(self.reset_pwd_url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)