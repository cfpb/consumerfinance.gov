from datetime import date
from unittest.mock import patch

from django.test import TestCase

from jobmanager.models.django import JobCategory
from jobmanager.models.pages import JobListingPage
from jobmanager.signals import register_signal_handlers
from v1.tests.wagtail_pages import helpers


class JobListingPagePublishedSignalCase(TestCase):
    def setUp(self):
        division = JobCategory.objects.create(job_category='category')
        self.page = JobListingPage(
            title='title1',
            salary_min='1',
            salary_max='2',
            description='description',
            open_date=date(2099, 1, 1),
            close_date=date(2099, 1, 15),
            division=division
        )

        register_signal_handlers()

    @patch('jobmanager.signals.flag_enabled', return_value=True)
    def test_ping_google_when_job_page_published(self, flag_enabled_check):
        with patch('requests.get') as mock_request:
            helpers.publish_page(child=self.page)
            mock_request.assert_called_once_with(
                'https://www.google.com/ping',
                {'sitemap': 'https://www.consumerfinance.gov/sitemap.xml'}
            )

    @patch('jobmanager.signals.flag_enabled', return_value=False)
    def test_ping_google_when_job_page_published_failure(
            self, flag_enabled_check):
        with patch('requests.get') as mock_request:
            helpers.publish_page(child=self.page)
            mock_request.assert_not_called()
