import os.path
import unittest
import zipfile
from six import StringIO
from zipfile import ZipFile

from django.core import management
from django.core.management.base import CommandError
from django.test import TestCase

import mock
from agreements.management.commands import _util
from agreements.management.commands.import_agreements import empty_folder_test
from agreements.models import Issuer


sample_zip = os.path.dirname(__file__) + '/sample-agreements.zip'
empty_folder_zip = os.path.dirname(__file__) + '/empty-folder-agreements.zip'
utf8_zip = os.path.dirname(__file__) + '/UTF_agreements.zip'


class EmptyFolderTest(unittest.TestCase):

    def test_empty_folder_test(self):
        agreements_zip = ZipFile(empty_folder_zip)
        all_pdfs = [name for name in agreements_zip.namelist()
                    if name.upper().endswith('.PDF')]
        blanks = empty_folder_test(agreements_zip, all_pdfs)
        self.assertEqual(blanks, ['Blank Folder/'])

    def test_import_agreements_raises_error(self):
        with self.assertRaises(CommandError):
            management.call_command(
                'import_agreements',
                '--path=' + empty_folder_zip,
                verbosity=0)


class TestDataLoad(TestCase):
    def test_import_no_s3(self):
        management.call_command(
            'import_agreements',
            '--path=' + sample_zip,
            '--windows',
            verbosity=0
        )
        self.assertEqual(Issuer.objects.all().count(), 2)

    def test_import_no_s3_utf8(self):
        management.call_command(
            'import_agreements',
            '--path=' + utf8_zip,
            verbosity=0
        )
        self.assertEqual(Issuer.objects.all().count(), 1)

    @mock.patch.dict(os.environ, {'AGREEMENTS_S3_UPLOAD_ENABLED': 'yes'})
    @mock.patch('agreements.management.commands.' +
                '_util.upload_to_s3')
    def test_import_with_s3(self, upload_func):
        management.call_command(
            'import_agreements',
            '--path=' + sample_zip,
            '--windows',
            verbosity=0
        )

        # this isn't great, but the dest_name changes to reflect the month
        # AND we can't predict the order agreements will be processed in.
        upload_func.assert_called()

    @mock.patch.dict(os.environ, {'AGREEMENTS_S3_UPLOAD_ENABLED': 'yes'})
    @mock.patch(
        'agreements.management.commands._util.upload_to_s3'
    )
    def test_import_with_s3_calls_print_statement(self, _):
        buf = StringIO()
        management.call_command(
            'import_agreements',
            '--path=' + sample_zip,
            '--windows',
            stdout=buf
        )
        self.assertIn('uploaded', buf.getvalue())


class TestManagementUtils(TestCase):

    def test_get_existing_issuer(self):
        management.call_command(
            'import_agreements',
            '--path=' + sample_zip,
            '--windows',
            verbosity=0
        )
        issuer = _util.get_issuer(u'Bankers\u2019 Bank of Kansas')
        self.assertEqual(issuer.slug, u'bankers-bank-of-kansas')

    def test_get_new_issuer(self):
        issuer = _util.get_issuer('2nd Fake Bank USA')
        self.assertEqual(issuer.slug, '2nd-fake-bank-usa')

    def test_save_agreement(self):
        agreements_zip = zipfile.ZipFile(sample_zip)
        # windows-1252 encoded:
        raw_path = b'Bankers\x92 Bank of Kansas/1.pdf'
        buf = StringIO()
        agreement = _util.save_agreement(
            agreements_zip,
            raw_path,
            buf,
            windows=True,
            upload=False)

        self.assertEqual(agreement.file_name, '1.pdf')

    @mock.patch.dict(os.environ, {'AWS_S3_ACCESS_KEY_ID': 'fake',
                                  'AWS_S3_SECRET_ACCESS_KEY': 'fake',
                                  'AWS_STORAGE_BUCKET_NAME': 'fake'})
    @mock.patch('boto3.client')
    def test_upload_to_s3(self, mock_upload):
        fake_pdf = StringIO("Not a real PDF")
        _util.upload_to_s3(fake_pdf, 'bank/agreement.pdf')
        mock_upload.assert_called_once()
