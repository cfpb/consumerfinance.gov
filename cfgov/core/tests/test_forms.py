from __future__ import unicode_literals

from django.test import TestCase, override_settings

from core.forms import ExternalURLForm
from core.utils import sign_url


@override_settings(
    EXTERNAL_URL_WHITELIST=(r'^https:\/\/facebook\.com\/cfpb$',)
)
class TestExternalURLForm(TestCase):
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

    def test_invalid_url_fails_validation(self):
        data = {'ext_url': 'foo'}
        form = ExternalURLForm(data)
        self.assertFalse(form.is_valid())

    def test_no_signature_fails_validation(self):
        data = {'ext_url': 'https://not.whitelisted.gov'}
        form = ExternalURLForm(data)
        self.assertFalse(form.is_valid())

    def test_unicode_url(self):
        url = 'https://cfpb.gov/protecci\xf3n'
        _, signature = sign_url(url)
        data = {'ext_url': url, 'signature': signature}

        with override_settings(EXTERNAL_URL_WHITELIST=(url,)):
            form = ExternalURLForm(data)
            self.assertTrue(form.is_valid())
