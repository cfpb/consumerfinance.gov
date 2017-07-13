from django.test import TestCase, override_settings

from legacy.views.housing_counselor import HousingCounselorView


@override_settings(AWS_STORAGE_BUCKET_NAME='foo.bucket')
class TestHousingCounselorView(TestCase):
    def test_s3_json_url(self):
        self.assertEqual(
            HousingCounselorView.s3_json_url(20001),
            'https://s3.amazonaws.com/foo.bucket/a/assets/hud/jsons/20001.json'
        )

    def test_s3_pdf_url(self):
        self.assertEqual(
            HousingCounselorView.s3_pdf_url(20009),
            'https://s3.amazonaws.com/foo.bucket/a/assets/hud/pdfs/20009.pdf'
        )
