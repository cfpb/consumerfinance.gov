from datetime import date

from django.test import TestCase

from mock import patch

from jobmanager.models.django import JobCategory, Region
from jobmanager.models.pages import JobListingPage
from v1.tests.wagtail_pages import helpers


class JobListingPagePublishedSignalCase(TestCase):
    def setUp(self):
        division = JobCategory(
            job_category="category"
        )
        division.save()
        region = Region(
            abbreviation="TS",
            name="TriStateArea"
        )
        region.save()
        self.page = JobListingPage(
            title='title1',
            salary_min='1',
            salary_max='2',
            description='description',
            open_date=date(2099, 1, 1),
            close_date=date(2099, 1, 15),
            division=division,
            location=region)

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
