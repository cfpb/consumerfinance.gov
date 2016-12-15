from django.test import TestCase, RequestFactory
from django.conf import settings

from core.utils import sign_url
from core.forms import ExternalURLForm


class TestExternalURLForm(TestCase):
    def setUp(self):
        # insulate the test from future whitelist changes
        self.preserved_whitelist = settings.EXTERNAL_URL_WHITELIST
        settings.EXTERNAL_URL_WHITELIST = (r'^https:\/\/facebook\.com\/cfpb$',)

    def test_valid_signature(self):
        url = 'https://https.cio.gov/'
        _, signature = sign_url(url)

        data = {'ext_url': url,
                'signature': signature}

        form = ExternalURLForm(data)

        self.assertTrue(form.is_valid())

    def test_invalid_signature(self):

        data = {'ext_url': 'https://https.cio.gov',
                'signature': 'obviouslywrong'}

        form = ExternalURLForm(data)

        self.assertFalse(form.is_valid())

    def test_whitelisted_url(self):
        data = {'ext_url': 'https://facebook.com/cfpb'}
        form = ExternalURLForm(data)

        self.assertTrue(form.is_valid())

    def test_url_not_in_whitelist(self):
        data = {'ext_url': 'http://google.com'}
        form = ExternalURLForm(data)

        self.assertFalse(form.is_valid())

    def tearDown(self):
        settings.EXTERNAL_URL_WHITELIST = self.preserved_whitelist
