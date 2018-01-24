import os.path
from cStringIO import StringIO
import zipfile

from django.core import management
from django.test import TestCase

import mock
from agreements.management.commands import util
from agreements.models import Issuer


sample_zip = os.path.dirname(__file__) + '/sample-agreements.zip'


class TestDataLoad(TestCase):
    def test_import_no_s3(self):
        management.call_command('import_agreements', '--path=' + sample_zip)
        self.assertEqual(Issuer.objects.all().count(), 2)

    @mock.patch.dict(os.environ, {'AGREEMENTS_S3_UPLOAD_ENABLED': 'yes'})
    @mock.patch('agreements.management.commands.' +
                'util.upload_to_s3')
    def test_import_with_s3(self, upload_func):
        management.call_command(
            'import_agreements',
            '--path=' + sample_zip,
            verbosity=0
        )

        # this isn't great, but the dest_name changes to reflect the month
        # AND we can't predict the order agreements will be processed in.
        upload_func.assert_called()

    @mock.patch.dict(os.environ, {'AGREEMENTS_S3_UPLOAD_ENABLED': 'yes'})
    @mock.patch(
        'agreements.management.commands.util.upload_to_s3'
    )
    def test_import_with_s3_calls_print_statement(self, _):
        buf = StringIO()
        management.call_command(
            'import_agreements',
            '--path=' + sample_zip,
            stdout=buf
        )
        self.assertIn('uploaded', buf.getvalue())


class TestManagementUtils(TestCase):

    def test_get_existing_issuer(self):
        management.call_command('import_agreements', '--path=' + sample_zip)
        issuer = util.get_issuer(u'Bankers\u2019 Bank of Kansas')
        self.assertEqual(issuer.slug, u'bankers-bank-of-kansas')

    def test_get_new_issuer(self):
        issuer = util.get_issuer('2nd Fake Bank USA')
        self.assertEqual(issuer.slug, '2nd-fake-bank-usa')

    def test_save_agreement(self):
        agreements_zip = zipfile.ZipFile(sample_zip)
        # windows-1252 encoded:
        raw_path = 'Bankers\x92 Bank of Kansas/1.pdf'
        buf = StringIO()
        agreement = util.save_agreement(
            agreements_zip,
            raw_path,
            'windows-1252',
            outfile=buf,
            upload=False)

        self.assertEqual(agreement.file_name, '1.pdf')

    @mock.patch.dict(os.environ, {'AWS_S3_ACCESS_KEY_ID': 'fake',
                                  'AWS_S3_SECRET_ACCESS_KEY': 'fake',
                                  'AWS_STORAGE_BUCKET_NAME': 'fake'})
    @mock.patch('boto3.client')
    def test_upload_to_s3(self, mock_upload):
        fake_pdf = StringIO("Not a real PDF")
        util.upload_to_s3(fake_pdf, 'bank/agreement.pdf')
        mock_upload.assert_called_once()
