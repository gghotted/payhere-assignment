from django.core.management import call_command
from django.test import TestCase
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

        dumpdata('base')
