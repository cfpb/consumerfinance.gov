from django.core.management import call_command
from django.test import TestCase, override_settings

from cdntools.backends import MOCK_PURGED


@override_settings(
    WAGTAILFRONTENDCACHE={
        "akamai": {
            "BACKEND": "cdntools.backends.MockCacheBackend",
        },
    }
)
class CacheTagPurgeTestCase(TestCase):
    def test_submission_with_url_akamai(self):
        call_command(
            "purge_by_cache_tags",
            "--cache_tag",
            "complaints",
            "--action",
            "invalidate",
        )
        self.assertIn("complaints", MOCK_PURGED)
