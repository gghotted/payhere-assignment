from datetime import timedelta

from account_books.models import Transaction
from core.schemas import *
from django.test import TestCase
from django.urls import reverse
from freezegun import freeze_time

from share.models import Guest


class GuestDetailAPITestCase(TestCase):
    fixtures = ['base']
    
    @classmethod
    def setUpTestData(cls):
        cls.guest = Guest.objects.first()
        cls.path = reverse('share:detail_guest', args=[cls.guest.code])

    def test_success(self):
        res = self.client.get(self.path)
        self.assertEqual(200, res.status_code)
        self.assertTrue(guest_schema.is_valid(res.json()))
    
    def test_is_expired(self):
        with freeze_time(self.guest.expired_at):
            res = self.client.get(self.path)
        self.assertEqual(False, res.json()['is_expired'])

        with freeze_time(self.guest.expired_at + timedelta(seconds=1)):
            res = self.client.get(self.path)
        self.assertEqual(True, res.json()['is_expired'])
