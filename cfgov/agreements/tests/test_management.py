import io
import os.path
import unittest
import zipfile
from unittest import mock

from django.core import management
from django.core.management.base import CommandError
from django.test import TestCase

from agreements.management.commands import _util
from agreements.models import Issuer

no_agreements_zip = os.path.dirname(__file__) + "/no-agreements.zip"
empty_folder_zip = os.path.dirname(__file__) + "/empty-folder-agreements.zip"
utf8_zip = os.path.dirname(__file__) + "/UTF_agreements.zip"
additional_directory = (
    os.path.dirname(__file__) + "/additional_directory_level.zip"
)  # noqa: B950


class TestValidations(unittest.TestCase):
    def test_no_agreements_causes_error(self):
        with self.assertRaises(CommandError):
            management.call_command(
                "import_agreements", "--path=" + no_agreements_zip, verbosity=0
            )

    def test_empty_folder_causes_error(self):
        with self.assertRaises(CommandError):
            management.call_command(
                "import_agreements", "--path=" + empty_folder_zip, verbosity=0
            )


class TestDataLoad(TestCase):
    def test_import_no_s3_utf8(self):
        management.call_command(
            "import_agreements", "--path=" + utf8_zip, verbosity=0
        )
        self.assertEqual(Issuer.objects.all().count(), 1)

    def test_import_2_directory_levels(self):
        management.call_command(
            "import_agreements", "--path=" + additional_directory, verbosity=0
        )
        self.assertEqual(Issuer.objects.all().count(), 1)

    @mock.patch.dict(os.environ, {"AGREEMENTS_S3_UPLOAD_ENABLED": "yes"})
    @mock.patch("agreements.management.commands._util.upload_to_s3")
    def test_import_with_s3_calls_print_statement(self, _):
        buf = io.StringIO()
        management.call_command(
            "import_agreements", "--path=" + utf8_zip, stdout=buf
        )
        self.assertIn("uploaded", buf.getvalue())


class TestManagementUtils(TestCase):
    def test_get_new_issuer(self):
        issuer = _util.get_issuer("2nd Fake Bank USA")
        self.assertEqual(issuer.slug, "2nd-fake-bank-usa")

    def test_save_agreement(self):
        agreements_zip = zipfile.ZipFile(utf8_zip)

        expectedName = "Visa Cardholder Agreement and Disclosures.pdf"
        raw_path = "UTF_agreements/" + expectedName

        buf = io.StringIO()
        agreement = _util.save_agreement(
            agreements_zip, raw_path, buf, upload=False
        )

        self.assertEqual(agreement.file_name, expectedName)

    @mock.patch.dict(
        os.environ,
        {
            "AWS_S3_ACCESS_KEY_ID": "fake",
            "AWS_S3_SECRET_ACCESS_KEY": "fake",
            "AWS_STORAGE_BUCKET_NAME": "fake",
        },
    )
    @mock.patch("boto3.client")
    def test_upload_to_s3(self, mock_upload):
        fake_pdf = io.StringIO("Not a real PDF")
        _util.upload_to_s3(fake_pdf, "bank/agreement.pdf")
        mock_upload.assert_called_once()

    def test_s3_safe_key(self):
        name = "Cardholder Agreement 3-5% cash back, Español"
        prefix = "/path/"
        expected = "/path/Cardholder_Agreement_3-5_cash_back_Español"
        self.assertEqual(_util.s3_safe_key(name, prefix), expected)
