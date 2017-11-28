import os.path

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
