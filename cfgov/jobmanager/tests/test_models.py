from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone
from mock import patch
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

    def test_save_sets_date_created_if_none(self):
        now = timezone.now()
        with patch('jobmanager.models.timezone.now', return_value=now):
            job = mommy.make(Job, date_created=None)
            self.assertEqual(job.date_created, now)

    def test_save_leaves_date_created_if_set(self):
        now = timezone.now()
        job = mommy.make(Job, date_created=now)
        self.assertEqual(job.date_created, now)
        job.save()
        self.assertEqual(job.date_created, now)

    def test_save_sets_date_modified(self):
        created = timezone.now()
        with patch('jobmanager.models.timezone.now', return_value=created):
            job = mommy.make(Job)
            self.assertEqual(job.date_modified, created)

        modified = timezone.now()
        with patch('jobmanager.models.timezone.now', return_value=modified):
            job.save()
            self.assertEqual(job.date_modified, modified)
