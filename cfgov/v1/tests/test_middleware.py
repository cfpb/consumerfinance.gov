from unittest import TestCase

from django.http import HttpRequest
from django.test import override_settings
from wagtail.wagtailcore.models import Site

from v1.middleware import StagingMiddleware


class StagingMiddlewareTestCase(TestCase):
    @override_settings(STAGING_HOSTNAME='content.localhost')
    def test_request_on_www(self):
        request = self.request_for_hostname('localhost')
        StagingMiddleware().process_request(request)
        self.assertFalse(request.is_staging)

    @override_settings(STAGING_HOSTNAME='content.localhost')
    def test_request_on_content(self):
        request = self.request_for_hostname('content.localhost')
        StagingMiddleware().process_request(request)
        self.assertTrue(request.is_staging)

    def request_for_hostname(self, hostname):
        request = HttpRequest()
        request.META['SERVER_NAME'] = hostname
        request.site = Site.objects.get(hostname=hostname)
        return request
