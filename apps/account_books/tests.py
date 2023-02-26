from core.schemas import *
from django.db.models.aggregates import Count
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from schema import Schema
from users.models import User
from users.tests import auth_header, create_token

from account_books.models import AccountBook


class AccountBookCreateAPIViewTestCase(TestCase):
    fixtures = ['base']
    path = reverse_lazy('users:list_account_book')

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.first()
        cls.token = create_token(cls.user)
        cls.header = auth_header(cls.token)

    def test_success(self):
        data = {'name': 'name'}
        res = self.client.post(
            self.path,
            data,
            **self.header,
        )
        self.assertEqual(201, res.status_code)
        self.assertTrue(create_response_schema.is_valid(res.json()))

    def test_too_short_name(self):
        data = {'name': 'a' * 2}
        res = self.client.post(
            self.path,
            data,
            **self.header,
        )
        self.assertEqual(400, res.status_code)

    def test_too_long_name(self):
        data = {'name': 'a' * 21}
        res = self.client.post(
            self.path,
            data,
            **self.header,
        )
        self.assertEqual(400, res.status_code)

    def test_no_auth(self):
        res = self.client.post(self.path)
        self.assertEqual(401, res.status_code)


class AccountBookListAPITestCase(TestCase):
    fixtures = ['base']
    path = reverse_lazy('users:list_account_book')

    @classmethod
    def setUpTestData(cls):
        cls.user = (
            User.objects
            .annotate(account_book_count=Count('account_books'))
            .filter(account_book_count__gte=1).first()
        )
        cls.token = create_token(cls.user)
        cls.header = auth_header(cls.token)

    def test_success(self):
        res = self.client.get(self.path, **self.header)
        self.assertEqual(200, res.status_code)
        self.assertTrue(
            Schema([account_book_schema]).is_valid(res.json())
        )

    def test_no_auth(self):
        res = self.client.get(self.path)
        self.assertEqual(401, res.status_code)


class AccountBookDetailAPITestCase(TestCase):
    fixtures = ['base']

    @classmethod
    def setUpTestData(cls):
        cls.account_book = AccountBook.objects.first()
        cls.user = cls.account_book.user
        cls.token = create_token(cls.user)
        cls.header = auth_header(cls.token)

        cls.path = reverse('account_books:detail', args=[cls.account_book.id])

    def test_success(self):
        res = self.client.get(self.path, **self.header)
        self.assertEqual(200, res.status_code)
        self.assertTrue(account_book_schema.is_valid(res.json()))

    def test_no_auth(self):
        res = self.client.get(self.path)
        self.assertEqual(401, res.status_code)
    
    def test_no_permission(self):
        user = User.objects.exclude(id=self.user.id).first()
        header = auth_header(create_token(user))

        res = self.client.get(self.path, **header)
        self.assertEqual(403, res.status_code)


class AccountBookUpdateAPITestCase(TestCase):
    fixtures = ['base']
    
    @classmethod
    def setUpTestData(cls):
        cls.account_book = AccountBook.objects.first()
        cls.user = cls.account_book.user
        cls.token = create_token(cls.user)
        cls.header = auth_header(cls.token)

        cls.path = reverse('account_books:detail', args=[cls.account_book.id])

    def test_success(self):
        input_data = {'name': 'update_name'}
        res = self.client.patch(
            self.path,
            input_data,
            'application/json',
            **self.header
        )
        self.assertEqual(200, res.status_code)

        res_data = res.json()
        self.assertTrue(account_book_schema.is_valid(res_data))
        self.assertEqual(res_data['name'], input_data['name'])

    def test_no_auth(self):
        res = self.client.patch(self.path)
        self.assertEqual(401, res.status_code)

    def test_no_permission(self):
        user = User.objects.exclude(id=self.user.id).first()
        header = auth_header(create_token(user))

        res = self.client.patch(self.path, **header)
        self.assertEqual(403, res.status_code)


class AccountBookDeleteAPIViewTestCase(TestCase):
    fixtures = ['base']

    @classmethod
    def setUpTestData(cls):
        cls.account_book = AccountBook.objects.first()
        cls.user = cls.account_book.user
        cls.token = create_token(cls.user)
        cls.header = auth_header(cls.token)

        cls.path = reverse('account_books:detail', args=[cls.account_book.id])

    def test_success(self):
        res = self.client.delete(self.path, **self.header)
        self.assertEqual(204, res.status_code)

    def test_no_auth(self):
        res = self.client.delete(self.path)
        self.assertEqual(401, res.status_code)

    def test_no_permission(self):
        user = User.objects.exclude(id=self.user.id).first()
        header = auth_header(create_token(user))

        res = self.client.delete(self.path, **header)
        self.assertEqual(403, res.status_code)
