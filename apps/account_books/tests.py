from datetime import timedelta

from core.schemas import *
from django.db.models.aggregates import Count
from django.forms.models import model_to_dict
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.utils.timezone import now
from freezegun import freeze_time
from schema import Schema
from users.models import User
from users.tests import auth_header, create_token

from account_books.models import AccountBook, Transaction


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


class TransactionCreateAPITestCase(TestCase):
    fixtures = ['base']
    
    @classmethod
    def setUpTestData(cls):
        cls.account_book = AccountBook.objects.first()
        cls.user = cls.account_book.user
        cls.token = create_token(cls.user)
        cls.header = auth_header(cls.token)

        cls.path = reverse(
            'account_books:list_transaction',
            args=[cls.account_book.id]
        )

    def setUp(self):
        self.data = {
            'description': 'buy pizza',
            'occurred_at': '2022-01-01',
            'amount': 5000,
            'type': '+',
        }

    def test_success(self):
        res = self.client.post(self.path, self.data, **self.header)
        self.assertEqual(201, res.status_code)
        self.assertTrue(create_response_schema.is_valid(res.json()))

    def test_not_allowed_type(self):
        self.data['type'] = '='
        res = self.client.post(self.path, self.data, **self.header)
        self.assertEqual(400, res.status_code)

    def test_min_amount(self):
        self.data['amount'] = 0
        res = self.client.post(self.path, self.data, **self.header)
        self.assertEqual(400, res.status_code)

    def test_no_auth(self):
        res = self.client.post(self.path)
        self.assertEqual(401, res.status_code)

    def test_no_permission(self):
        user = User.objects.exclude(id=self.user.id).first()
        header = auth_header(create_token(user))

        res = self.client.post(self.path, **header)
        self.assertEqual(403, res.status_code)


class TransactionListAPITestCase(TestCase):
    fixtures = ['base']
    
    @classmethod
    def setUpTestData(cls):
        cls.account_book = (
            AccountBook.objects
            .annotate(transaction_count=Count('transactions'))
            .filter(transaction_count__gte=10).first()
        )
        cls.user = cls.account_book.user
        cls.token = create_token(cls.user)
        cls.header = auth_header(cls.token)

        cls.path = reverse(
            'account_books:list_transaction',
            args=[cls.account_book.id]
        )

    def test_success(self):
        res = self.client.get(self.path, **self.header)
        self.assertEqual(200, res.status_code)
        self.assertTrue(
            wrap_pagination_schema(transaction_schema).is_valid(res.json())
        )

    def test_no_auth(self):
        res = self.client.get(self.path)
        self.assertEqual(401, res.status_code)

    def test_no_permission(self):
        user = User.objects.exclude(id=self.user.id).first()
        header = auth_header(create_token(user))

        res = self.client.get(self.path, **header)
        self.assertEqual(403, res.status_code)


class TransactionDetailAPITestCase(TestCase):
    fixtures = ['base']

    @classmethod
    def setUpTestData(cls):
        cls.trans = Transaction.objects.first()
        cls.user = cls.trans.account_book.user
        cls.token = create_token(cls.user)
        cls.header = auth_header(cls.token)

        cls.path = reverse(
            'account_books:detail_transaction',
            args=[
                cls.trans.account_book.id,
                cls.trans.id,
            ]
        )

    def test_success(self):
        res = self.client.get(self.path, **self.header)
        self.assertEqual(200, res.status_code)
        self.assertTrue(transaction_schema.is_valid(res.json()))

    def test_no_auth(self):
        res = self.client.get(self.path)
        self.assertEqual(401, res.status_code)

    def test_no_permission(self):
        user = User.objects.exclude(id=self.user.id).first()
        header = auth_header(create_token(user))

        res = self.client.get(self.path, **header)
        self.assertEqual(403, res.status_code)

    def _create_guest_code(self):
        res = self.client.post(
            self.path + 'share-links/',
            **self.header,
        )
        url = res.json()['url']
        guest_code = url.split('/')[-1]
        return guest_code

    def test_success_guest(self):
        guest_code = self._create_guest_code()

        res = self.client.get(self.path + '?guest=%s' % guest_code)
        self.assertEqual(200, res.status_code)

    def test_expired_guest(self):
        time = now()
        with freeze_time(time):
            guest_code = self._create_guest_code()

        with freeze_time(time + timedelta(days=1, seconds=1)):
            res = self.client.get(self.path + '?guest=%s' % guest_code)

        self.assertEqual(401, res.status_code)

    def test_wrong_guest_code(self):
        res = self.client.get(self.path + '?guest=abcd')
        self.assertEqual(401, res.status_code)


class TransactionUpdateAPITestCase(TestCase):
    fixtures = ['base']

    @classmethod
    def setUpTestData(cls):
        cls.trans = Transaction.objects.filter(type='+').first()
        cls.user = cls.trans.account_book.user
        cls.token = create_token(cls.user)
        cls.header = auth_header(cls.token)

        cls.path = reverse(
            'account_books:detail_transaction',
            args=[
                cls.trans.account_book.id,
                cls.trans.id,
            ]
        )

    def test_success(self):
        input_data = {
            'description': 'update description',
            'amount': 9999,
            'type': '-',
        }
        res = self.client.patch(
            self.path,
            input_data,
            'application/json',
            **self.header,
        )
        self.assertEqual(200, res.status_code)

        res_data = res.json()
        self.assertTrue(transaction_schema.is_valid(res_data))

        self.trans.refresh_from_db()
        self.assertEqual(
            input_data,
            model_to_dict(self.trans, fields=input_data.keys())
        )

    def test_no_auth(self):
        res = self.client.patch(self.path)
        self.assertEqual(401, res.status_code)

    def test_no_permission(self):
        user = User.objects.exclude(id=self.user.id).first()
        header = auth_header(create_token(user))

        res = self.client.patch(self.path, **header)
        self.assertEqual(403, res.status_code)

    def test_not_allowed_method_guest(self):
        res = self.client.post(
            self.path + 'share-links/',
            **self.header,
        )
        url = res.json()['url']
        guest_code = url.split('/')[-1]

        res = self.client.patch(self.path + '?guest=%s' % guest_code)
        self.assertEqual(401, res.status_code)


class TransactionDeleteAPITestCase(TestCase):
    fixtures = ['base']

    @classmethod
    def setUpTestData(cls):
        cls.trans = Transaction.objects.first()
        cls.user = cls.trans.account_book.user
        cls.token = create_token(cls.user)
        cls.header = auth_header(cls.token)

        cls.path = reverse(
            'account_books:detail_transaction',
            args=[
                cls.trans.account_book.id,
                cls.trans.id,
            ]
        )
    
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

    def test_not_allowed_method_guest(self):
        res = self.client.post(
            self.path + 'share-links/',
            **self.header,
        )
        url = res.json()['url']
        guest_code = url.split('/')[-1]

        res = self.client.delete(self.path + '?guest=%s' % guest_code)
        self.assertEqual(401, res.status_code)


class TransactionCopyAPITestCase(TestCase):
    fixtures = ['base']

    @classmethod
    def setUpTestData(cls):
        cls.trans = Transaction.objects.first()
        cls.user = cls.trans.account_book.user
        cls.token = create_token(cls.user)
        cls.header = auth_header(cls.token)

        cls.path = reverse(
            'account_books:copy_transaction',
            args=[
                cls.trans.account_book.id,
                cls.trans.id,
            ]
        )

    def test_success(self):
        res = self.client.post(self.path, **self.header)
        self.assertEqual(201, res.status_code)

        data = res.json()
        self.assertTrue(create_response_schema.is_valid(data))

        copied_trans = Transaction.objects.get(id=data['id'])
        check_fields = [
            'account_book',
            'description',
            'occurred_at',
            'amount',
            'type',
        ]
        self.assertEqual(
            model_to_dict(self.trans, fields=check_fields),
            model_to_dict(copied_trans, fields=check_fields),
        )
        self.assertNotEqual(self.trans.id, copied_trans.id)

    def test_no_auth(self):
        res = self.client.post(self.path)
        self.assertEqual(401, res.status_code)

    def test_no_permission(self):
        user = User.objects.exclude(id=self.user.id).first()
        header = auth_header(create_token(user))

        res = self.client.post(self.path, **header)
        self.assertEqual(403, res.status_code)


class TransactionShareAPITestCase(TestCase):
    fixtures = ['base']

    @classmethod
    def setUpTestData(cls):
        cls.trans = Transaction.objects.first()
        cls.user = cls.trans.account_book.user
        cls.token = create_token(cls.user)
        cls.header = auth_header(cls.token)

        cls.path = reverse(
            'account_books:share_transaction',
            args=[
                cls.trans.account_book.id,
                cls.trans.id,
            ]
        )

    def test_success(self):
        res = self.client.post(self.path, **self.header)
        self.assertEqual(200, res.status_code)

        url = res.json()['url']
        self.assertTrue(url.startswith('https://front.com/s/'))

        guest_code = url.split('/')[-1]
        self.assertEqual(12, len(guest_code))

    def test_no_auth(self):
        res = self.client.post(self.path)
        self.assertEqual(401, res.status_code)

    def test_no_permission(self):
        user = User.objects.exclude(id=self.user.id).first()
        header = auth_header(create_token(user))

        res = self.client.post(self.path, **header)
        self.assertEqual(403, res.status_code)
