from unittest import mock

from django.core.management import call_command
from django.test import TestCase, override_settings


@override_settings(
    WAGTAILFRONTENDCACHE={
        "akamai": {
            "BACKEND": "v1.models.caching.AkamaiBackend",
            "CLIENT_TOKEN": "fake",
            "CLIENT_SECRET": "fake",
            "ACCESS_TOKEN": "fake",
        }
    }
)
class InvalidateAllPagesTestCase(TestCase):
    @mock.patch("v1.models.caching.AkamaiBackend.purge_all")
    def test_submission_with_url_akamai(self, mock_purge_all):
        call_command("invalidate_all_pages_cache")
        mock_purge_all.assert_any_call()
