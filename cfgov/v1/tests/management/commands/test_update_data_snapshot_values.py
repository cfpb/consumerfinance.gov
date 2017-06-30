from django.core.management import call_command
from django.test import Client, TestCase

from wagtail.wagtailcore.blocks import StreamValue

from scripts import _atomic_helpers as atomic
from v1.models.browse_page import BrowsePage
from v1.tests.wagtail_pages.helpers import publish_page

django_client = Client()

class UpdateDataSnapshotValuesTestCase(TestCase):
        def test_data_snapshot(self):
            """ Data Snapshot correctly renders fields on a Browse Page"""
            browse_page = BrowsePage(
                title='Browse Page',
                slug='browse',
            )

            # Adds a AUT market to a browse page
            browse_page.content = StreamValue(
                browse_page.content.stream_block,
                [atomic.data_snapshot],
                True
            )
            publish_page(child=browse_page)

            # Call management command to update values
            call_command('update_data_snapshot_values', '--snapshot_file=v1/tests/fixtures/data_snapshots.json')
            response = self.client.get('/browse/')
            self.assertContains(response, '2.1 million')
            self.assertContains(response, '$46.4 billion')
            self.assertContains(response, '5.8% increase')
            self.assertContains(response, 'April 2017')
            self.assertContains(response, 'Auto loans originated')
            self.assertContains(response, 'Dollar value of new loans')
            self.assertContains(response, 'In year-over-year originations')
