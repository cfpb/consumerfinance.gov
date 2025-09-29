from io import StringIO

from django.core.management import call_command
from django.test import TestCase, override_settings

from cdntools.backends import MOCK_PURGED


@override_settings(
    WAGTAILFRONTENDCACHE={
        "akamai": {
            "BACKEND": "cdntools.backends.MockAkamaiBackend",
        },
        "other": {
            "BACKEND": "cdntools.backends.MockBackend",
        },
    }
)
class PurgeCacheTestCase(TestCase):
    def test_purge_with_url(self):
        call_command(
            "purge_cache",
            url=[
                "https://server/foo",
                "https://server/bar",
            ],
        )
        self.assertIn("https://server/bar", MOCK_PURGED)
        self.assertIn("https://server/foo", MOCK_PURGED)

    def test_purge_with_cache_tag(self):
        call_command(
            "purge_cache",
            "--backend",
            "akamai",
            cache_tag=[
                "complaints",
                "foo",
            ],
        )
        self.assertIn("complaints", MOCK_PURGED)
        self.assertIn("foo", MOCK_PURGED)

    def test_purge_with_cache_tag_not_supported(self):
        err = StringIO()
        call_command(
            "purge_cache",
            "--backend",
            "other",
            cache_tag=[
                "complaints",
                "foo",
            ],
            stderr=err,
        )
        self.assertIn("Cannot purge tags from backend: other", err.getvalue())

    def test_purge_all(self):
        call_command("purge_cache", "--all", "--backend", "akamai")
        self.assertIn("__all__", MOCK_PURGED)

    def test_purge_all_not_supported(self):
        err = StringIO()
        call_command("purge_cache", "--all", "--backend", "other", stderr=err)
        self.assertIn("Cannot purge all from backend: other", err.getvalue())

    def test_purge_nebackend(self):
        err = StringIO()
        with self.assertRaises(SystemExit):
            call_command(
                "purge_cache",
                "--all",
                "--backend",
                "noneexistent",
                stderr=err,
            )
        self.assertIn(
            "Frontend cache backends are not configured: noneexistent",
            err.getvalue(),
        )

    def test_purge_with_empty(self):
        err = StringIO()
        call_command(
            "purge_cache",
            stderr=err,
        )
        self.assertIn(
            "Please provide one or more of --all/--url/--cache_tag",
            err.getvalue(),
        )
