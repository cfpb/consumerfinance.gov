from django.db import IntegrityError
from django.test import TestCase
from model_mommy import mommy

from jobmanager.models import Job


class JobTestCase(TestCase):
    def test_slug_uniqueness(self):
        mommy.make(Job, slug='abcde')
        with self.assertRaises(IntegrityError):
            mommy.make(Job, slug='abcde')

    def test_slug_case_sensitive_uniqueness(self):
        mommy.make(Job, slug='abcde')
        mommy.make(Job, slug='ABCDE')
