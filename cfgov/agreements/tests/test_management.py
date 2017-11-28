import os.path

import mock

from django.core import management
from django.test import TestCase

from agreements.models import Agreement, Issuer


class TestDataLoad(TestCase):
    def test_import_no_s3(self):
        sample_dir = os.path.dirname(__file__) + '/sample_credit_agreements'
        management.call_command('import_agreements', '--path=' + sample_dir)
        self.assertEqual(Issuer.objects.all()[0].name,
                         '1st Financial Bank USA')
        self.assertEqual(Agreement.objects.all()[1].file_name,
                         'Some Agreement.pdf')

    @mock.patch.dict(os.environ, {'AGREEMENTS_S3_UPLOAD_ENABLED': 'yes'})
    @mock.patch('agreements.management.commands.' +
                'import_agreements.upload_to_s3')
    def test_import_with_s3(self, upload_func):
        sample_dir = os.path.dirname(__file__) + '/sample_credit_agreements'
        management.call_command('import_agreements', '--path=' + sample_dir)

        full_file_path = sample_dir +\
            '/1st Financial Bank USA/Some Agreement.pdf'
        s3_dest_path =\
            '/a/assets/credit-card-agreements/pdf/11_2017_Some Agreement.pdf'

        upload_func.assert_called_with(file_path=full_file_path,
                                       s3_dest_path=s3_dest_path)
