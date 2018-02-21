from django.test import TestCase
from mock import patch
import mock
from datetime import date
import os

from v1.tests.wagtail_pages import helpers

from jobmanager.models.django import JobCategory, Region
from jobmanager.models.pages import JobListingPage

ENV_VARS = {
    'GOOGLE_PING_URL': 'http://www.google-url.com',
    'SITEMAP_URL': 'http://www.sitemap-url.com'
}


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

    @mock.patch.dict(os.environ, ENV_VARS)
    def test_ping_google_when_job_page_published(self):
        with patch('requests.get') as mock_request:
            helpers.publish_page(child=self.page)
            mock_request.assert_called_once_with(
                ENV_VARS['GOOGLE_PING_URL'],
                {'sitemap': ENV_VARS['SITEMAP_URL']}
            )

    @mock.patch.dict(os.environ, {})
    def test_ping_google_when_job_page_published_failure(self):
        with patch('requests.get') as mock_request:
            helpers.publish_page(child=self.page)
            mock_request.assert_not_called()
