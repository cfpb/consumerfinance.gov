from django.core.exceptions import ValidationError
from django.test import TestCase

from mock import patch
from model_mommy import mommy

from jobmanager.models.django import Grade, JobCategory, JobRegion
from jobmanager.models.pages import JobListingPage
from jobmanager.models.panels import GradePanel
from v1.tests.wagtail_pages.helpers import save_new_page


class JobListingPageTestCase(TestCase):
    def setUp(self):
        self.division = mommy.make(JobCategory)
        self.region = mommy.make(JobRegion)

        page_clean = patch('jobmanager.models.pages.CFGOVPage.clean')
        page_clean.start()
        self.addCleanup(page_clean.stop)

    def prepare_job_listing_page(self, **kwargs):
        kwargs.setdefault('description', 'default')
        kwargs.setdefault('division', self.division)
        kwargs.setdefault('region', self.region)
        return mommy.prepare(JobListingPage, **kwargs)

    def test_clean_with_all_fields_passes_validation(self):
        page = self.prepare_job_listing_page()
        try:
            page.full_clean()
        except ValidationError:
            self.fail('clean with all fields should validate')

    def test_clean_without_description_fails_validation(self):
        page = self.prepare_job_listing_page(description=None)
        with self.assertRaises(ValidationError):
            page.full_clean()

    def test_clean_without_open_date_fails_validation(self):
        page = self.prepare_job_listing_page(open_date=None)
        with self.assertRaises(ValidationError):
            page.full_clean()

    def test_clean_without_close_date_fails_validation(self):
        page = self.prepare_job_listing_page(close_date=None)
        with self.assertRaises(ValidationError):
            page.full_clean()

    def test_clean_without_salary_min_fails_validation(self):
        page = self.prepare_job_listing_page(salary_min=None)
        with self.assertRaises(ValidationError):
            page.full_clean()

    def test_clean_without_salary_max_fails_validation(self):
        page = self.prepare_job_listing_page(salary_max=None)
        with self.assertRaises(ValidationError):
            page.full_clean()

    def test_clean_without_division_fails_validation(self):
        page = self.prepare_job_listing_page(division=None)
        with self.assertRaises(ValidationError):
            page.full_clean()

    def make_page_with_grades(self, *grades):
        page = self.prepare_job_listing_page()
        save_new_page(page)

        for grade in grades:
            panel = GradePanel.objects.create(
                grade=mommy.make(Grade, grade=str(grade)),
                job_listing=page
            )
            page.grades.add(panel)

        return page

    def test_ordered_grades(self):
        page = self.make_page_with_grades('3', '2', '1')
        self.assertEqual(page.ordered_grades, ['1', '2', '3'])

    def test_ordered_grades_removes_duplicates(self):
        page = self.make_page_with_grades('3', '2', '2', '2', '1', '1')
        self.assertEqual(page.ordered_grades, ['1', '2', '3'])

    def test_ordered_grades_sorts_numerically(self):
        page = self.make_page_with_grades('100', '10', '11', '1')
        self.assertEqual(page.ordered_grades, ['1', '10', '11', '100'])

    def test_ordered_grades_non_numeric_after_numeric(self):
        page = self.make_page_with_grades('2', '1', 'b', 'B', 'a', 'A')
        self.assertEqual(page.ordered_grades, ['1', '2', 'A', 'B', 'a', 'b'])

    def test_ordered_grades_returns_strings(self):
        page = self.make_page_with_grades('3', '2', '1')
        for grade in page.ordered_grades:
            self.assertIsInstance(grade, basestring)
