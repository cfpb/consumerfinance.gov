from unittest import mock

from django.test import TestCase, override_settings

import requests

from housing_counselor.views import (
    HousingCounselorS3URLMixin,
    HousingCounselorView,
)


@override_settings(
    AWS_STORAGE_BUCKET_NAME="foo.bucket", AWS_S3_CUSTOM_DOMAIN="bar.bucket"
)
class HousingCounselorS3URLMixinTestCase(TestCase):
    def test_s3_json_url(self):
        self.assertEqual(
            HousingCounselorS3URLMixin.s3_json_url(20001),
            "https://s3.amazonaws.com/foo.bucket/a/assets/hud/jsons/20001.json",
        )

    def test_s3_pdf_url(self):
        self.assertEqual(
            HousingCounselorS3URLMixin.s3_pdf_url(20009),
            "https://bar.bucket/a/assets/hud/pdfs/20009.pdf",
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
            HousingCounselorView.invalid_zip_msg["invalid_zip_error_message"],
        )

    @mock.patch("housing_counselor.views.HousingCounselorView.get_counselors")
    def test_get_counselors_failed_s3_request(self, mock_get_counselors):
        mock_get_counselors.side_effect = requests.exceptions.ConnectionError
        response = self.client.get("/find-a-housing-counselor/?zipcode=12345")
        self.assertNotIn("zipcode_valid", response.context_data)
        self.assertNotIn("api_json", response.context_data)
        self.assertNotIn("pdf_url", response.context_data)
        self.assertContains(
            response,
            HousingCounselorView.failed_fetch_msg[
                "failed_fetch_error_message"
            ],
        )

    @mock.patch("housing_counselor.views.HousingCounselorView.get_counselors")
    def test_get_counselors_invalid_zipcode(self, mock_get_counselors):
        self.client.get("/find-a-housing-counselor/", {"zipcode": "abcdef"})
        mock_get_counselors.assert_not_called()

    @mock.patch("housing_counselor.views.HousingCounselorView.get_counselors")
    def test_get_counselors_valid_zipcode(self, mock_get_counselors):
        mock_get_counselors.return_value = {}
        response = self.client.get(
            "/find-a-housing-counselor/", {"zipcode": "12345"}
        )
        self.assertTrue(response.context_data["zipcode_valid"])
        self.assertIn("12345.pdf", response.context_data["pdf_url"])
