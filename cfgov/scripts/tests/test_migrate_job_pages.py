from decimal import Decimal
from django.test import TestCase
from model_mommy import mommy
from wagtail.wagtailcore.models import Page

from jobmanager.models.django import Job
from scripts.migrate_job_pages import JobConverter


class JobConverterTestCase(TestCase):
    def convert_job(self, job):
        parent_page = Page.objects.get(slug='cfgov')
        converter = JobConverter(parent=parent_page)
        return converter.convert(job)

    def test_convert_job_keeps_slug(self):
        job = mommy.make(Job)
        page = self.convert_job(job)
        self.assertEqual(job.slug, page.slug)

    def test_convert_job_keeps_title(self):
        job = mommy.make(Job)
        page = self.convert_job(job)
        self.assertEqual(job.title, page.title)

    def test_convert_job_keeps_open_date(self):
        job = mommy.make(Job)
        page = self.convert_job(job)
        self.assertEqual(job.open_date, page.open_date)

    def test_convert_job_keeps_close_date(self):
        job = mommy.make(Job)
        page = self.convert_job(job)
        self.assertEqual(job.close_date, page.close_date)

    def test_convert_job_keeps_salary_min(self):
        job = mommy.make(Job, salary_min=Decimal('123.45'))
        page = self.convert_job(job)
        self.assertEqual(job.salary_min, page.salary_min)

    def test_convert_job_keeps_salary_max(self):
        job = mommy.make(Job, salary_max=Decimal('123.45'))
        page = self.convert_job(job)
        self.assertEqual(job.salary_max, page.salary_max)

    def test_convert_job_sets_division(self):
        job = mommy.make(Job)
        page = self.convert_job(job)
        self.assertEqual(job.category, page.division)
