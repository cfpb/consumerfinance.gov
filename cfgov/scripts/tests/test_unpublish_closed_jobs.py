import json
from datetime import date

from django.test import TestCase

import requests
from mock import Mock, patch
from scripts import unpublish_closed_jobs

from jobmanager.models.django import ApplicantType, JobCategory, Region
from jobmanager.models.pages import JobListingPage
from jobmanager.models.panels import USAJobsApplicationLink
from v1.tests.wagtail_pages import helpers


class UnpublishClosedJobsTestCase(TestCase):
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
        self.public_type = ApplicantType(
            applicant_type="public",
            description="description"
        )
        self.public_type.save()
        self.status_type = ApplicantType(
            applicant_type="status",
            description="description"
        )
        self.status_type.save()
        self.page = JobListingPage(
            title='title1',
            salary_min='1',
            salary_max='2',
            description='description',
            open_date=date(2099, 1, 1),
            close_date=date(2099, 1, 15),
            division=division,
            location=region,
            live=True)
        helpers.publish_page(child=self.page)

    def create_job_link(self, control_number, applicant_type):
        job_link = USAJobsApplicationLink(
            announcement_number=control_number,
            applicant_type=applicant_type,
            url='http://www.test.com/{}'.format(control_number),
            job_listing=self.page
        )
        job_link.save()
        return job_link

    def api_not_found_job_response(self):
        mock_response = Mock()
        mock_response.status_code = 200
        text = {
            "SearchResult": {
                "SearchResultCount": 0,
                "SearchResultItems": []
            }
        }
        mock_response.text = json.dumps(text)
        return mock_response

    def api_closed_job_response(self, control_number):
        mock_response = Mock()
        mock_response.status_code = 200
        text = {
            "SearchResult": {
                "SearchResultCount": 1,
                "SearchResultItems": [
                    {"MatchedObjectId": control_number}
                ]
            }
        }
        mock_response.text = json.dumps(text)
        return mock_response

    def open_usajobs_page(self):
        mock_response = Mock(
            status_code=200,
            text='<html></html>'
        )
        return mock_response

    def closed_usajobs_page(self):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = (
            '<html>'
            '<div class="usajobs-joa-closed">'
            'This job announcement has closed'
            '</div>'
            '</html>'
        )
        return mock_response

    @patch('requests.get')
    def test_job_listing_page_still_live_if_job_not_closed_on_api(
            self, request_mock):
        self.assertTrue(self.page.live)

        control_number = '1'
        self.create_job_link(control_number, self.public_type)
        request_mock.return_value = self.api_not_found_job_response()

        unpublish_closed_jobs.run()
        self.page.refresh_from_db()

        request_mock.assert_called_once()
        args, kwargs = request_mock.call_args
        self.assertEqual(
            kwargs['params'],
            {'ControlNumber': control_number, 'WhoMayApply': 'all'}
        )
        self.assertTrue(self.page.live)
        self.assertFalse(self.page.expired)

    @patch('requests.get')
    def test_job_listing_page_still_live_if_job_page_not_closed(
            self, request_mock):
        self.assertTrue(self.page.live)

        control_number = '1'
        job_link = self.create_job_link(control_number, self.status_type)
        request_mock.return_value = self.open_usajobs_page()

        unpublish_closed_jobs.run()
        self.page.refresh_from_db()

        request_mock.assert_called_once_with(job_link.url)

        self.assertTrue(self.page.live)
        self.assertFalse(self.page.expired)

    @patch('requests.get')
    def test_job_listing_page_unpublished_if_job_closed_on_usajobs(
            self, request_mock):
        self.assertTrue(self.page.live)
        control_number = '1'
        job_link = self.create_job_link(control_number, self.status_type)
        request_mock.return_value = self.closed_usajobs_page()

        unpublish_closed_jobs.run()
        self.page.refresh_from_db()

        request_mock.assert_called_once_with(job_link.url)
        self.assertFalse(self.page.live)
        self.assertTrue(self.page.expired)

    @patch('requests.get')
    def test_job_listing_page_unpublished_if_job_archived(
            self, request_mock):
        self.assertTrue(self.page.live)
        control_number = '1'

        self.create_job_link(control_number, self.public_type)
        request_mock.return_value = self.api_closed_job_response(
            control_number
        )

        unpublish_closed_jobs.run()
        self.page.refresh_from_db()

        self.assertFalse(self.page.live)
        self.assertTrue(self.page.expired)

    @patch('requests.get')
    def test_job_listing_page_live_if_only_1_of_2_links_closed(
            self, request_mock):
        self.assertTrue(self.page.live)

        def side_effect(*args, **kwargs):
            if str(args[0]).startswith('http://www.test.com'):
                return self.open_usajobs_page()
            return self.api_closed_job_response('1')

        self.create_job_link('1', self.public_type)
        self.create_job_link('2', self.status_type)
        request_mock.side_effect = side_effect

        unpublish_closed_jobs.run()
        self.page.refresh_from_db()

        self.assertTrue(self.page.live)
        self.assertFalse(self.page.expired)

    @patch('requests.get')
    def test_job_listing_page_unpublished_if_all_links_closed(
            self, request_mock):
        self.assertTrue(self.page.live)

        def side_effect(*args, **kwargs):
            if str(args[0]).startswith('http://www.test.com'):
                return self.closed_usajobs_page()
            return self.api_closed_job_response('1')

        self.create_job_link('1', self.public_type)
        self.create_job_link('2', self.status_type)
        request_mock.side_effect = side_effect

        unpublish_closed_jobs.run()
        self.page.refresh_from_db()
        self.assertFalse(self.page.live)
        self.assertTrue(self.page.expired)

    @patch('scripts.unpublish_closed_jobs.logger.exception')
    @patch('requests.get')
    def test_api_check_failure(self, request_mock, logger_mock):
        self.assertTrue(self.page.live)

        job_link = self.create_job_link('1', self.public_type)
        request_mock.side_effect = requests.exceptions.ConnectionError
        with self.assertRaises(SystemExit):
            unpublish_closed_jobs.run()

        self.page.refresh_from_db()
        logger_mock.assert_called_with(
            'API check for job "{}" failed'.format(job_link.url)
        )
        self.assertTrue(self.page.live)

    @patch('scripts.unpublish_closed_jobs.logger.exception')
    @patch('requests.get')
    def test_page_check_failure(self, request_mock, logger_mock):
        self.assertTrue(self.page.live)
        job_link = self.create_job_link('1', self.status_type)
        request_mock.side_effect = Exception
        with self.assertRaises(SystemExit):
            unpublish_closed_jobs.run()

        self.page.refresh_from_db()
        logger_mock.assert_called_with(
            'Check of USAJobs page "{}" failed'.format(job_link.url)
        )
        self.assertTrue(self.page.live)
