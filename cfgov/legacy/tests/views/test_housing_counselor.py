from django.test import TestCase, override_settings

import mock
import requests

from legacy.views.housing_counselor import HousingCounselorS3URLMixin


@override_settings(AWS_STORAGE_BUCKET_NAME='foo.bucket')
class HousingCounselorS3URLMixinTestCase(TestCase):
    def test_s3_json_url(self):
        self.assertEqual(
            HousingCounselorS3URLMixin.s3_json_url(20001),
            'https://s3.amazonaws.com/foo.bucket/a/assets/hud/jsons/20001.json'
        )

    def test_s3_pdf_url(self):
        self.assertEqual(
            HousingCounselorS3URLMixin.s3_pdf_url(20009),
            'https://s3.amazonaws.com/foo.bucket/a/assets/hud/pdfs/20009.pdf'
        )


@override_settings(AWS_STORAGE_BUCKET_NAME='foo.bucket')
class HousingCounselorViewTestCase(TestCase):

    @mock.patch('requests.get')
    def test_get_counselors_failed_s3_request(self, mock_requests_get):
        mock_requests_get.side_effect = requests.HTTPError
        response = self.client.get('/find-a-housing-counselor/')
        self.assertNotIn('zipcode_valid', response.context)
        self.assertNotIn('api_json', response.context)
        self.assertNotIn('pdf_url', response.context)

    @mock.patch('requests.get')
    def test_get_counselors_invalid_zipcode(self, mock_requests_get):
        self.client.get('/find-a-housing-counselor/', {'zipcode': 'abcdef'})
        mock_requests_get.assert_not_called()

    @mock.patch('requests.get')
    def test_get_counselors_valid_zipcode(self, mock_requests_get):
        mock_requests_get.return_value.json.return_value = {}
        response = self.client.get('/find-a-housing-counselor/',
                                   {'zipcode': '12345'})
        self.assertTrue(response.context['zipcode_valid'])
        self.assertIn('12345.pdf', response.context['pdf_url'])

    @mock.patch('requests.get')
    def test_get_counselors_pdf_template(self, mock_requests_get):
        mock_requests_get.return_value.json.return_value = {}
        response = self.client.get('/find-a-housing-counselor/', {'pdf': ''})
        self.assertIn('pdf', response.templates[0].name)


@override_settings(AWS_STORAGE_BUCKET_NAME='foo.bucket')
class HousingCounselorPDFViewTestCase(TestCase):

    def test_get_invalid_form(self):
        response = self.client.get('/save-hud-counselors-list/', {})
        self.assertEqual(response.status_code, 400)

    def test_get_valid_form(self):
        response = self.client.get('/save-hud-counselors-list/',
                                   {'zip': '12345'})
        self.assertEqual(response.status_code, 302)
