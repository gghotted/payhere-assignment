from core.schemas import *
from django.test import TestCase
from django.urls import reverse_lazy

from users.models import User


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
