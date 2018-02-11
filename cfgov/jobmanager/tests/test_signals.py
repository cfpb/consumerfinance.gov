from django.test import TestCase
from mock import patch

from datetime import date

from v1.tests.wagtail_pages import helpers

from jobmanager.models.django import JobCategory, Region
from jobmanager.models.pages import JobListingPage


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

    @patch('flags.state.flag_enabled', return_value=True)
    @patch('requests.get')
    def ping_google_when_job_listing_page_published_if_flag_true(
            self, google_ping, flag_enabled_check):
        helpers.publish_page(child=self.page)
        google_ping.assert_called_once_with(
            'http://www.google.com/ping',
            {'sitemap': 'https://www.consumerfinance.gov/sitemap.xml'}
        )

    @patch('flags.state.flag_enabled', return_value=False)
    @patch('requests.get')
    def google_not_alerted_when_job_listing_page_published_if_flag_false(
            self, google_ping, flag_enabled_check):
        helpers.publish_page(child=self.page)
        google_ping.assert_not_called()
