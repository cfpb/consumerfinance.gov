from unittest import mock

from django.core.management import call_command
from django.test import TestCase


class CacheTagPurgeTestCase(TestCase):

    @mock.patch("v1.signals.AkamaiBackend.purge_by_tags")
    def test_submission_with_url_akamai(self, mock_purge_tags):
        call_command(
            "purge_by_cache_tags",
            "--cache_tag", "complaints",
            "--action", "invalidate",
        )
        self.assertTrue(mock_purge_tags.called_with(
            "complaints",
            action="invalidate"
        ))
