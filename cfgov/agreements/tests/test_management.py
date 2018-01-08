import os.path
from cStringIO import StringIO

from django.core import management
from django.test import TestCase

import mock
from agreements.management.commands import util
from agreements.models import Agreement, Issuer


sample_dir = os.path.dirname(__file__) + '/sample_credit_agreements'


class TestDataLoad(TestCase):
    def test_import_no_s3(self):
        management.call_command('import_agreements', '--path=' + sample_dir)
        self.assertEqual(Issuer.objects.all()[0].name,
                         '1st Financial Bank USA')
        agreement_names = [a.file_name for a in Agreement.objects.all()]
        self.assertIn('Some Agreement.pdf', agreement_names)

    @mock.patch.dict(os.environ, {'AGREEMENTS_S3_UPLOAD_ENABLED': 'yes'})
    @mock.patch('agreements.management.commands.' +
                'import_agreements.upload_to_s3')
    def test_import_with_s3(self, upload_func):
        management.call_command(
            'import_agreements',
            '--path=' + sample_dir,
            verbosity=0
        )

        # this isn't great, but the dest_name changes to reflect the month
        # AND we can't predict the order agreements will be processed in.
        upload_func.assert_called()

    @mock.patch.dict(os.environ, {'AGREEMENTS_S3_UPLOAD_ENABLED': 'yes'})
    @mock.patch(
        'agreements.management.commands.import_agreements.upload_to_s3'
    )
    def test_import_with_s3_calls_print_statement(self, _):
        buf = StringIO()
        management.call_command(
            'import_agreements',
            '--path=' + sample_dir,
            stdout=buf
        )
        self.assertIn('uploaded to', buf.getvalue())


class TestManagementUtils(TestCase):
    def test_clear_tables(self):
        util.clear_tables()
        self.assertEqual(len(Agreement.objects.all()), 0)

    def test_get_file_size(self):

        empty_pdf = sample_dir +\
            '/1st Financial Bank USA/Some Agreement.pdf'
        size = util.get_file_size(empty_pdf)
        self.assertEqual(size, 0)

    def test_update_existing_issuer(self):
        management.call_command('import_agreements', '--path=' + sample_dir)
        util.update_issuer('1st Financial Bank USA')
        # This is basically a no-op, there's nothing to assert

    def test_new_issuer(self):
        issuer = util.update_issuer('2nd Financial Bank USA')
        self.assertEqual(issuer.slug, '2nd-financial-bank-usa')

    def test_duplicate_issuer(self):
        issuer_name = '2nd Financial Bank USA'
        issuer_slug = '2nd-financial-bank-usa'
        util.update_issuer(issuer_name)
        duplicate = Issuer(name=issuer_name,
                           slug=issuer_slug)
        duplicate.save()
        # unfortunately general, but it correctly
        # captures the current logic:
        with self.assertRaises(Exception):
            util.update_issuer(issuer_name)

    def test_existing_agreement(self):
        management.call_command('import_agreements', '--path=' + sample_dir)
        issuer = util.update_issuer('1st Financial Bank USA')
        file_path = sample_dir + '/1st Financial Bank USA/Some Agreement.pdf'
        util.update_agreement(
            issuer=issuer,
            file_path=file_path,
            file_name='agreement.pdf',
            s3_location='http://www.consumerfinance.gov')
        # This is basically a no-op, there's nothing to assert

    def test_new_agreement(self):
        management.call_command('import_agreements', '--path=' + sample_dir)
        issuer = util.update_issuer('1st Financial Bank USA')
        file_path = sample_dir + '/1st Financial Bank USA/Some Agreement.pdf'
        agreement = util.update_agreement(
            issuer=issuer,
            file_path=file_path,
            file_name='agreement2.pdf',
            s3_location='http://www.consumerfinance.gov')

        self.assertEqual(agreement.file_name, 'agreement2.pdf')

    def test_duplicate_agreement(self):
        management.call_command('import_agreements', '--path=' + sample_dir)
        issuer = util.update_issuer('1st Financial Bank USA')
        file_path = sample_dir + '/1st Financial Bank USA/Some Agreement.pdf'
        util.update_agreement(
            issuer=issuer,
            file_path=file_path,
            file_name='agreement2.pdf',
            s3_location='http://www.consumerfinance.gov')

        duplicate = Agreement(
            file_name='agreement2.pdf',
            issuer=issuer,
            size=0,
            uri='https://www.consumerfinance.gov',)
        duplicate.save()
        # unfortunately general, but it correctly
        # captures the current logic:
        with self.assertRaises(Exception):
            util.update_agreement(
                issuer=issuer,
                file_path=file_path,
                file_name='agreement2.pdf',
                s3_location='http://www.consumerfinance.gov')

    @mock.patch.dict(os.environ, {'AWS_S3_ACCESS_KEY_ID': 'fake',
                                  'AWS_S3_SECRET_ACCESS_KEY': 'fake',
                                  'AWS_STORAGE_BUCKET_NAME': 'fake'})
    @mock.patch('tinys3.Connection.upload')
    def test_upload_to_s3(self, mock_upload):
        file_path = sample_dir + '/1st Financial Bank USA/Some Agreement.pdf'
        util.upload_to_s3(file_path, 'agreement.pdf')
        mock_upload.assert_called_once()
