from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings
from django.contrib.auth.models import User

import mock


cache_config = {'BACKEND': 'v1.models.akamai_backend.AkamaiBackend',
                'CLIENT_TOKEN': 'fake',
                'CLIENT_SECRET': 'fake',
                'ACCESS_TOKEN': 'fake'}


@override_settings(WAGTAILFRONTENDCACHE=dict(akamai=cache_config))
class TestCDNManagementView(TestCase):
    def setUp(self):

        self.superuser = User.objects.create_superuser(username='superuser',
                                                       email='',
                                                       password='password')

    def test_requires_authentication(self):
        response = self.client.get(reverse('manage-cdn'))
        expected_url = 'http://testserver/admin/login/?next=/admin/cdn/'
        self.assertRedirects(response,
                             expected_url,
                             fetch_redirect_response=False)

    def test_superuser(self):
        self.client.login(username='superuser', password='password')
        response = self.client.get(reverse('manage-cdn'))
        self.assertEqual(response.status_code, 200)

    @mock.patch('v1.models.akamai_backend.AkamaiBackend.purge')
    def test_submission_with_url(self, mock_purge):
        self.client.login(username='superuser', password='password')
        self.client.post(reverse('manage-cdn'),
                         {'url': 'http://fake.gov'})
        mock_purge.assert_called_with('http://fake.gov')

    @mock.patch('v1.models.akamai_backend.AkamaiBackend.purge_all')
    def test_submission_without_url(self, mock_purge_all):
        self.client.login(username='superuser', password='password')
        self.client.post(reverse('manage-cdn'))
        mock_purge_all.assert_any_call()

    def test_bad_submission(self):
        self.client.login(username='superuser', password='password')
        response = self.client.post(reverse('manage-cdn'),
                                    {'url': 'not a URL'})
        self.assertContains(response, "url: Enter a valid URL.")


class TestCDNManagerNotEnabled(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(username='superuser',
                                                       email='',
                                                       password='password')

    def test_cdnmanager_not_enabled(self):
        self.client.login(username='superuser', password='password')
        response = self.client.get(reverse('manage-cdn'))
        expected_message = "CDN management is not currently enabled"
        self.assertContains(response, expected_message)
