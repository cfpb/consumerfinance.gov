from django.test import TestCase

from v1.models.akamai_backend import AkamaiBackend

class TestAkamaiBackend(TestCase):
    def test_no_credentials_raises(self):
        credentials = {
                'CLIENT_TOKEN': None,
                'CLIENT_SECRET': None,
                'ACCESS_TOKEN': None,
                'FAST_PURGE_URL': None,
        }
        with self.assertRaises(ValueError):
            AkamaiBackend(credentials)

    def test_some_credentials_raises(self):
        credentials = {
                'CLIENT_TOKEN': 'some-arbitrary-token',
                'CLIENT_SECRET': None,
                'ACCESS_TOKEN': None,
                'FAST_PURGE_URL': None,
        }
        with self.assertRaises(ValueError):
            AkamaiBackend(credentials)

    def test_all_credentials_get_set(self):
        credentials = {
                'CLIENT_TOKEN': 'token',
                'CLIENT_SECRET': 'secret',
                'ACCESS_TOKEN': 'access token',
                'FAST_PURGE_URL': 'fast purge url',
        }
        akamai_backend = AkamaiBackend(credentials)
        self.assertEquals(akamai_backend.client_token, 'token')
        self.assertEquals(akamai_backend.client_secret, 'secret')
        self.assertEquals(akamai_backend.access_token, 'access token')
        self.assertEquals(akamai_backend.fast_purge_url, 'fast purge url')