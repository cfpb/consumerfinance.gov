from unittest import mock

from django.core.management import call_command
from django.test import TestCase, override_settings


@override_settings(
    WAGTAILFRONTENDCACHE={
        "akamai": {
            "BACKEND": "cdntools.backends.AkamaiBackend",
            "CLIENT_TOKEN": "fake",
            "CLIENT_SECRET": "fake",
            "ACCESS_TOKEN": "fake",
        }
    }
)
class InvalidateAllPagesTestCase(TestCase):
    @mock.patch("cdntools.backends.AkamaiBackend.purge_all")
    def test_submission_with_url_akamai(self, mock_purge_all):
        call_command("invalidate_all_pages_cache")
        mock_purge_all.assert_any_call()
