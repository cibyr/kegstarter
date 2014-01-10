from decimal import Decimal

from django.test import TestCase

from django.contrib.auth.models import User
from django.utils.timezone import utc

from datetime import datetime, timedelta

from main.models import KegMaster
from main.views import get_current_kegmaster


class KegMasterTestCase(TestCase):
    fixtures = ['basic.json']

    def setUp(self):
        self.kegop = User.objects.get(username='kegop')
        self.drinker = User.objects.get(username='drinker')
        self.now = datetime.utcnow().replace(tzinfo=utc)

    def testEmptyTable(self):
        self.assertIsNone(get_current_kegmaster())

    def testOneKegMasterTable(self):
        only_master = KegMaster()
        only_master.user = self.kegop
        only_master.start = self.now
        only_master.end = None
        only_master.save()
        self.assertEqual(get_current_kegmaster(), only_master)

    def testMultipleKegMasterTable1(self):
        first_master = KegMaster()
        first_master.user = self.kegop
        first_master.start = self.now - timedelta(days=1)
        first_master.end = self.now
        first_master.save()
        second_master = KegMaster()
        second_master.user = self.drinker
        second_master.start = self.now
        second_master.end = None
        second_master.save()
        self.assertEqual(get_current_kegmaster(), second_master)

    def testMultipleKegMasterTable2(self):
        first_master = KegMaster()
        first_master.user = self.kegop
        first_master.start = self.now - timedelta(days=1)
        first_master.end = None
        first_master.save()
        second_master = KegMaster()
        second_master.user = self.drinker
        second_master.start = self.now
        second_master.end = None
        second_master.save()
        self.assertEqual(get_current_kegmaster(), second_master)

    def testMultipleKegMasterTable2(self):
        first_master = KegMaster()
        first_master.user = self.kegop
        first_master.start = self.now - timedelta(days=2)
        first_master.end = self.now - timedelta(days=1)
        first_master.save()
        second_master = KegMaster()
        second_master.user = self.drinker
        second_master.start = self.now - timedelta(days=1)
        second_master.end = self.now - timedelta(seconds=1)
        second_master.save()
        self.assertEqual(get_current_kegmaster(), None)

    def testMultipleKegMasterTable3(self):
        first_master = KegMaster()
        first_master.user = self.kegop
        first_master.start = self.now - timedelta(days=2)
        first_master.end = self.now - timedelta(days=1)
        first_master.save()
        second_master = KegMaster()
        second_master.user = self.drinker
        second_master.start = self.now - timedelta(days=1)
        second_master.end = self.now + timedelta(seconds=1)
        second_master.save()
        self.assertEqual(get_current_kegmaster(), second_master)

    def testMultipleKegMasterTable4(self):
        first_master = KegMaster()
        first_master.user = self.kegop
        first_master.start = self.now - timedelta(days=1)
        first_master.end = self.now - timedelta(seconds=1)
        first_master.save()
        second_master = KegMaster()
        second_master.user = self.drinker
        second_master.start = self.now - timedelta(days=1)
        second_master.end = self.now + timedelta(seconds=1)
        second_master.save()
        self.assertEqual(get_current_kegmaster(), second_master)

    def testMultipleKegMasterTable5(self):
        first_master = KegMaster()
        first_master.user = self.kegop
        first_master.start = self.now - timedelta(days=1)
        first_master.end = self.now + timedelta(seconds=1)
        first_master.save()
        second_master = KegMaster()
        second_master.user = self.drinker
        second_master.start = self.now - timedelta(days=1)
        second_master.end = self.now - timedelta(seconds=1)
        second_master.save()
        self.assertEqual(get_current_kegmaster(), first_master)