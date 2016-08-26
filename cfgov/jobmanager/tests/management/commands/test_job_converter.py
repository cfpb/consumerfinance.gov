from decimal import Decimal
from django.test import TestCase
from mock import patch
from model_mommy import mommy
from wagtail.wagtailcore.models import Page

from jobmanager.management.commands.convert_jobs_to_wagtail import JobConverter
from jobmanager.models.django import Job
from jobmanager.models.pages import JobListingPage


class JobConverterTestCase(TestCase):
    def setUp(self):
        patched_print = patch(
            'jobmanager.management.commands.convert_jobs_to_wagtail.print'
        )
        patched_print.start()
        self.addCleanup(patched_print.stop)

    def test_create_with_parent(self):
        try:
            JobConverter('home-page')
        except Page.DoesNotExist:
            self.fail('creation with existing parent should not fail')

    def test_create_with_missing_parent(self):
        self.assertRaises(Page.DoesNotExist, JobConverter, 'no-such-page')

    def convert_job(self, job, commit=False):
        converter = JobConverter('home-page', commit=commit)
        return converter.convert(job)

    def test_convert_job_without_commit_does_not_make_page(self):
        self.assertFalse(JobListingPage.objects.exists())

        job = mommy.make(Job)
        self.convert_job(job, commit=False)

        self.assertFalse(JobListingPage.objects.exists())

    def test_convert_job_with_commit_makes_page(self):
        self.assertFalse(JobListingPage.objects.exists())

        job = mommy.make(Job)
        self.convert_job(job, commit=True)

        self.assertTrue(JobListingPage.objects.exists())
        self.assertEqual(JobListingPage.objects.count(), 1)

    def test_convert_job_keeps_slug(self):
        job = mommy.make(Job)
        page = self.convert_job(job, commit=True)
        self.assertEqual(job.slug, page.slug)

    def test_convert_job_keeps_title(self):
        job = mommy.make(Job)
        page = self.convert_job(job, commit=True)
        self.assertEqual(job.title, page.title)

    def test_convert_job_keeps_open_date(self):
        job = mommy.make(Job)
        page = self.convert_job(job, commit=True)
        self.assertEqual(job.open_date, page.open_date)

    def test_convert_job_keeps_close_date(self):
        job = mommy.make(Job)
        page = self.convert_job(job, commit=True)
        self.assertEqual(job.close_date, page.close_date)

    def test_convert_job_keeps_salary_min(self):
        job = mommy.make(Job, salary_min=Decimal('123.45'))
        page = self.convert_job(job, commit=True)
        self.assertEqual(job.salary_min, page.salary_min)

    def test_convert_job_keeps_salary_max(self):
        job = mommy.make(Job, salary_max=Decimal('123.45'))
        page = self.convert_job(job, commit=True)
        self.assertEqual(job.salary_max, page.salary_max)

    def test_convert_job_sets_division(self):
        job = mommy.make(Job)
        page = self.convert_job(job, commit=True)
        self.assertEqual(job.category, page.division)
