from core.fixtures import USER_PASSWORD
from core.schemas import *
from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User


def create_user(email='email@google.com', password='password1234'):
    user = User.objects.create_user(
        email=email,
        password=password,
    )
    user._password = password
    return user


def create_token(user):
    serializer = TokenObtainPairSerializer(
        data={
            'email': user.email,
            'password': USER_PASSWORD,
        }
    )
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data


def auth_header(token):
    return {'HTTP_AUTHORIZATION': f'Bearer {token["access"]}'} 


class UserCreateAPITestCase(TestCase):
    path = reverse_lazy('users:create')

    @classmethod
    def setUpTestData(cls):
        cls.exist_user = User.objects.create_user(
            email='exist@google.com',
            password='password1234',
        )

    def setUp(self):
        self.data = {
            'email': 'payhere@google.com',
            'password': 'password1234',
            'password2': 'password1234',
        }

    def test_url(self):
        self.assertEqual('/users/', self.path)

    def test_success(self):
        res = self.client.post(self.path, self.data)
        self.assertEqual(201, res.status_code)
        self.assertTrue(create_response_schema.is_valid(res.json()))

    def test_exist_email(self):
        self.data['email'] = self.exist_user.email
        res = self.client.post(self.path, self.data)
        self.assertEqual(400, res.status_code)

    def test_mismatch_password(self):
        self.data['password2'] = self.data['password2'][:-1]
        res = self.client.post(self.path, self.data)
        self.assertEqual(400, res.status_code)


class TokenCreateAPIViewTestCase(TestCase):
    path = reverse_lazy('auth:create_token')

    @classmethod
    def setUpTestData(cls):
        cls.password = 'password1234'
        cls.user = User.objects.create_user(
            email='user@google.com',
            password=cls.password,
        )

    def test_url(self):
        self.assertEqual('/auth/tokens/', self.path)

    def test_success(self):
        data = {
            'email': self.user.email,
            'password': self.password,
        }
        res = self.client.post(self.path, data)
        self.assertEqual(200, res.status_code)
        self.assertTrue(token_schema.is_valid(res.json()))


class TokenRefreshAPITestCase(TestCase):
    path = reverse_lazy('auth:refresh_token')

    @classmethod
    def setUpTestData(cls):
        cls.user = create_user()
        cls.tokens = create_token(cls.user)

    def test_url(self):
        self.assertEqual('/auth/tokens/refresh/', self.path)
    
    def test_success(self):
        data = {
            'refresh': self.tokens['refresh'],
        }
        res = self.client.post(self.path, data)
        self.assertEqual(200, res.status_code)
        self.assertTrue('access' in res.json())


class TokenBlackAPITestCase(TestCase):
    path = reverse_lazy('auth:blacklist_token')

    @classmethod
    def setUpTestData(cls):
        cls.user = create_user()
        cls.tokens = create_token(cls.user)

    def test_url(self):
        self.assertEqual('/auth/tokens/blacklist/', self.path)

    def test_success(self):
        data = {
            'refresh': self.tokens['refresh'],
        }
        res = self.client.post(self.path, data)
        self.assertEqual(200, res.status_code)
