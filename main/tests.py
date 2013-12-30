from decimal import Decimal

from django.test import TestCase

from django.contrib.auth.models import User

from .models import Keg, Donation, Vote, Purchase
from .views import get_user_balance, fund_context

class BalanceTestCase(TestCase):
    fixtures = ['basic.json']

    def setUp(self):
        self.kegop = User.objects.get(username='kegop')
        self.drinker = User.objects.get(username='drinker')
        self.keg = Keg.objects.get()

    def testInitiallyNoBalance(self):
        self.assertEqual(get_user_balance(self.kegop), 0)
        self.assertEqual(get_user_balance(self.drinker), 0)
        context = fund_context()
        self.assertEqual(context['total_donations'], 0)
        self.assertEqual(context['spent'], 0)
        self.assertEqual(context['balance'], 0)

    def testDonationBalance(self):
        Donation(user=self.drinker, amount=1, recipient=self.kegop).save()
        self.assertEqual(get_user_balance(self.kegop), 0)
        self.assertEqual(get_user_balance(self.drinker), 1)
        context = fund_context()
        self.assertEqual(context['total_donations'], 1)
        self.assertEqual(context['spent'], 0)
        self.assertEqual(context['balance'], 1)
        Donation(user=self.kegop, amount=99, recipient=self.kegop).save()
        self.assertEqual(get_user_balance(self.kegop), 99)
        self.assertEqual(get_user_balance(self.drinker), 1)
        context = fund_context()
        self.assertEqual(context['total_donations'], 100)
        self.assertEqual(context['spent'], 0)
        self.assertEqual(context['balance'], 100)

    def testNoFractionalVotes(self):
        Donation(user=self.drinker, amount=0.2, recipient=self.kegop).save()
        self.assertEqual(get_user_balance(self.kegop), 0)
        self.assertEqual(get_user_balance(self.drinker), 0)
        context = fund_context()
        self.assertEqual(context['total_donations'], Decimal('0.20'))
        self.assertEqual(context['spent'], 0)
        self.assertEqual(context['balance'], Decimal('0.20'))
        Donation(user=self.drinker, amount=0.5, recipient=self.kegop).save()
        self.assertEqual(get_user_balance(self.kegop), 0)
        self.assertEqual(get_user_balance(self.drinker), 0)
        context = fund_context()
        self.assertEqual(context['total_donations'], Decimal('0.70'))
        self.assertEqual(context['spent'], 0)
        self.assertEqual(context['balance'], Decimal('0.70'))
        Donation(user=self.drinker, amount=0.3, recipient=self.kegop).save()
        self.assertEqual(get_user_balance(self.kegop), 0)
        self.assertEqual(get_user_balance(self.drinker), 1)
        context = fund_context()
        self.assertEqual(context['total_donations'], 1)
        self.assertEqual(context['spent'], 0)
        self.assertEqual(context['balance'], 1)

    def testSpending(self):
        Donation(user=self.drinker, amount=200, recipient=self.kegop).save()
        context = fund_context()
        self.assertEqual(context['total_donations'], 200)
        self.assertEqual(context['spent'], 0)
        self.assertEqual(context['balance'], 200)
        Purchase(user=self.kegop, keg=self.keg).save()
        context = fund_context()
        self.assertEqual(context['total_donations'], 200)
        self.assertEqual(context['spent'], 123)
        self.assertEqual(context['balance'], 77)

    def testSpendingVotes(self):
        Donation(user=self.drinker, amount=1, recipient=self.kegop).save()
        Vote(user=self.drinker, keg=self.keg, value=1).save()
        self.assertEqual(get_user_balance(self.drinker), 0)
        Donation(user=self.drinker, amount=100, recipient=self.kegop).save()
        self.assertEqual(get_user_balance(self.drinker), 100)
        Vote(user=self.drinker, keg=self.keg, value=1).save()
        self.assertEqual(get_user_balance(self.drinker), 99)
        Vote(user=self.drinker, keg=self.keg, value=99).save()
        self.assertEqual(get_user_balance(self.drinker), 0)
