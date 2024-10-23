from django.core.management import call_command
from django.test import TestCase, override_settings

from cdntools.backends import MOCK_PURGED


@override_settings(
    WAGTAILFRONTENDCACHE={
        "akamai": {
            "BACKEND": "cdntools.backends.MockCacheBackend",
        }
    }
)
class InvalidatePageTestCase(TestCase):
    def test_submission_with_url(self):
        call_command(
            "invalidate_page_cache",
            url=[
                "https://server/foo/bar",
            ],
        )
        self.assertIn("https://server/foo/bar", MOCK_PURGED)
