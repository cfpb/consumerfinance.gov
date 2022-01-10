from unittest import mock

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings


class DeletePageCacheTestCase(TestCase):
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
    @mock.patch(
        "v1.management.commands.delete_page_cache.purge_urls_from_cache"
    )
    def test_submission_with_url_akamai(self, mock_purge):
        call_command("delete_page_cache", url="https://server/foo/bar")
        mock_purge.assert_called_once_with(
            "https://server/foo/bar",
            backend_settings={
                "akamai_deleting": {
                    "BACKEND": "v1.models.caching.AkamaiDeletingBackend",
                    "CLIENT_TOKEN": "fake",
                    "CLIENT_SECRET": "fake",
                    "ACCESS_TOKEN": "fake"
                }
            },
            backends=["akamai_deleting"]
        )

    def test_rasies_command_error_without_akamai_config(self):
        with self.assertRaises(CommandError):
            call_command("delete_page_cache", url="https://server/foo/bar")
