from account_books.models import AccountBook, Transaction
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.test import TestCase
from share.models import Guest
from users.models import User

USER_PASSWORD = 'password1234'


def dumpdata(name):
    path = 'core/fixtures/%s.json' % name
    call_command(
        'dumpdata',
        '--indent', '4'
        ,'-o', path
    )


class FixtureGenerateBase(TestCase):

    def test_gernerate(self):
        '''
        유저 2명이 있습니다.
        '''
        user1 = User.objects.create_user(
            'user1@google.com',
            USER_PASSWORD,
        )
        user2 = User.objects.create_user(
            'user2@google.com',
            USER_PASSWORD,
        )

        '''
        user1은 1개의 AccountBook을 가집니다.
        이 AccountBook는 15개의 transaction을 가집니다.
        이 transaction중 1개는 guest를 가집니다.
        '''
        account_book = AccountBook.objects.create(
            user=user1,
            name='name',
        )
        transactions = [
            Transaction(
                account_book=account_book,
                description='description',
                occurred_at='2023-01-01',
                amount=5000,
                type=('+' if i < 7 else '-'),
            )
            for i in range(15)
        ]
        transactions = Transaction.objects.bulk_create(transactions)
        trans = transactions[0]
        guest = Guest.objects.create(
            created_by=trans.account_book.user,
            access_scope='view transaction %d' % trans.id,
            expired_at='2099-01-01',
            object_pks={
                'transaction': trans.id,
                'account_book': trans.account_book.id,
            },
        )
        dumpdata('base')
