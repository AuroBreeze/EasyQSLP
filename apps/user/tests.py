from unittest import SkipTest

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User_Login, Email_Verify_Code,User_Profile
from django.contrib.auth import get_user_model
from django.utils import timezone
import datetime

User = get_user_model()

class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('user:register')
        self.valid_payload = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpassword',
            'code': '123456',
        }
        # 创建一个验证码
        Email_Verify_Code.objects.update_or_create(
            email='test@example.com',
            defaults={
                'code': '123456',
                'send_time': timezone.now(),
                'expire_time': timezone.now() + timezone.timedelta(minutes=5),
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

@SkipTest
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
        #print(response_refresh_vaile.json())
        self.assertEqual(response_refresh_vaile.status_code, status.HTTP_200_OK)
        self.assertIn('access', response_refresh_vaile.json())
        self.assertIn('refresh', response_refresh_vaile.json())

        response_verify_vaile = self.client.post(self.jwt_token_verify_url, {'token': response.json()['access']}, format='json')
        #print(response_verify_vaile.json())
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
        #print(response.json())
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


@SkipTest
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

@SkipTest
class UserEmailCodeSendTestCase(TestCase):


    def setUp(self):
        self.client = APIClient()
        self.email_code_send_url = reverse('user:emailsendcode')
        self.user = User_Login.objects.create_user(email='test@example.com', username='testuser',
                                                   password='testpassword')
        self.valid_payload = {
            'email': 'test@example.com',
            'usage': 'ResetPassword'
        }
    def test_valid_user_email_code_send_ResetPassword(self):
        response = self.client.post(self.email_code_send_url,self.valid_payload,format='json')
        #print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.json()['success'])
        self.assertEqual(response.json()['message'], 'Email code sent successfully!')

    def test_valid_user_email_code_send_Register(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload['usage'] = 'Register'
        invalid_payload['email'] = 'test123@example.com'
        response = self.client.post(self.email_code_send_url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.json()['success'])
        self.assertEqual(response.json()['message'], 'Email code sent successfully!')

    def test_invalid_user_email_code_send_ResetPassword(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload['email'] = 'test123@example.com'
        response = self.client.post(self.email_code_send_url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.json()['success'])
        self.assertIn('message', response.json())

    def test_invalid_user_email_code_send_Register(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload['usage'] = 'Register'
        response = self.client.post(self.email_code_send_url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.json()['success'])
        self.assertIn('message', response.json())

@SkipTest
class UserProfileTestCase(TestCase):
    def setUp(self):
        self.client:APIClient = APIClient()
        self.user = User_Login.objects.create_user(email='test@example.com', username='testuser',
                                                   password='testpassword')
        self.profile_url = reverse('user:revise-profile')
        self.get_profile_url = reverse('user:user-profile',args=[self.user.pk])
        self.token_url = reverse('user:token')

        self.valid_payload = {
            'birthday': '2000-01-01',
            'introduction': 'test introduction',
            'sex': "MALE",
        }
    def test_valid_update_user_profile(self):
        token = self.client.post(self.token_url,{'email':'test@example.com','password':'testpassword'},format='json').json()
        #print(token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token['access'])
        response = self.client.post(self.profile_url,self.valid_payload,format='json')
        #print(response.json())
        #查看鉴权
        #print(response.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json()['success'])
        self.assertEqual(
            User_Profile.objects.filter(user_Login=self.user).first().birthday,
            datetime.date.fromisoformat(self.valid_payload['birthday'])
        )
        self.assertEqual(User_Profile.objects.filter(user_Login=self.user).first().introduction,self.valid_payload['introduction'])
        self.assertEqual(User_Profile.objects.filter(user_Login=self.user).first().sex,self.valid_payload['sex'])

    def test_invalid_update_user_profile(self):
        self.client.force_authenticate(user=self.user)
        User_Profile.objects.update_or_create(user_Login=self.user,defaults={
            'birthday': '2000-01-01',
            'introduction': 'test introduction',
        })
        invalid_payload = self.valid_payload.copy()
        invalid_payload['birthday'] = '2000-01-01'
        invalid_payload['introduction'] = 'test introduction'
        invalid_payload['sex'] = "male"
        response = self.client.post(self.profile_url,invalid_payload,format='json')
        #print(response.json())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.json()['success'])
    def test_valid_unauthorized_update_user_profile(self):
        response = self.client.post(self.profile_url,self.valid_payload,format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        #self.assertFalse(response.json()['success'])
        self.assertIn('detail',response.json())
    def test_get_user_profile(self):
        self.client.force_authenticate(user=self.user)
        User_Profile.objects.update_or_create(user_Login=self.user,defaults={
            'birthday': '2000-01-01',
            'introduction': 'test introduction',
        })

        response = self.client.get(self.get_profile_url,args=[self.user.pk])
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json()['success'])
        #self.assertEqual(response.json()['data']['birthday'],'2000-01-01')
        self.assertEqual(response.json()['data']['introduction'],'test introduction')



