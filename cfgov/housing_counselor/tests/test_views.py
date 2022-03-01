from unittest import mock

from django.test import TestCase, override_settings

import requests

from housing_counselor.views import (
    HousingCounselorS3URLMixin,
    HousingCounselorView,
)


class HousingCounselorS3URLMixinTestCase(TestCase):
    def test_s3_json_url(self):
        self.assertEqual(
            HousingCounselorS3URLMixin.s3_json_url(20001),
            "https://s3.amazonaws.com/files.consumerfinance.gov/a/assets/hud/jsons/20001.json",  # noqa: B950
        )

    def test_s3_pdf_url(self):
        self.assertEqual(
            HousingCounselorS3URLMixin.s3_pdf_url(20009),
            "https://s3.amazonaws.com/files.consumerfinance.gov/a/assets/hud/pdfs/20009.pdf",  # noqa: B950
        )


@override_settings(AWS_STORAGE_BUCKET_NAME="foo.bucket")
class HousingCounselorViewTestCase(TestCase):
    @mock.patch("housing_counselor.views.HousingCounselorView.get_counselors")
    def test_get_counselors_request_nonexistent_zip(self, mock_get_counselors):
        mock_get_counselors.side_effect = requests.HTTPError
        response = self.client.get("/find-a-housing-counselor/?zipcode=00000")
        self.assertNotIn("zipcode_valid", response.context_data)
        self.assertNotIn("api_json", response.context_data)
        self.assertNotIn("pdf_url", response.context_data)
        self.assertContains(
            response,
            HousingCounselorView.invalid_zip_msg["error_message"],
        )

    @mock.patch("housing_counselor.views.HousingCounselorView.get_counselors")
    def test_get_counselors_failed_s3_request(self, mock_get_counselors):
        mock_get_counselors.side_effect = requests.exceptions.ConnectionError
        response = self.client.get("/find-a-housing-counselor/?zipcode=12345")
        self.assertNotIn("zipcode_valid", response.context_data)
        self.assertNotIn("api_json", response.context_data)
        self.assertNotIn("pdf_url", response.context_data)
        self.assertContains(
            response, HousingCounselorView.failed_fetch_msg["error_message"]
        )

    @mock.patch("housing_counselor.views.HousingCounselorView.get_counselors")
    def test_get_counselors_invalid_zipcode(self, mock_get_counselors):
        self.client.get("/find-a-housing-counselor/", {"zipcode": "abcdef"})
        mock_get_counselors.assert_not_called()

    @mock.patch("housing_counselor.views.HousingCounselorView.get_counselors")
    def test_get_counselors_valid_zipcode(self, mock_get_counselors):
        mock_get_counselors.return_value = {}
        response = self.client.get("/find-a-housing-counselor/", {"zipcode": "12345"})
        self.assertTrue(response.context_data["zipcode_valid"])
        self.assertIn("12345.pdf", response.context_data["pdf_url"])


@override_settings(AWS_STORAGE_BUCKET_NAME="foo.bucket")
class HousingCounselorPDFViewTestCase(TestCase):
    def test_get_invalid_form(self):
        response = self.client.get("/save-hud-counselors-list/", {})
        self.assertEqual(response.status_code, 400)

    def test_get_valid_form(self):
        response = self.client.get("/save-hud-counselors-list/", {"zip": "12345"})
        self.assertEqual(response.status_code, 302)
