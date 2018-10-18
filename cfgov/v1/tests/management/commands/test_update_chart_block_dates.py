import os

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase

from wagtail.wagtailcore.blocks import StreamValue

from scripts import _atomic_helpers as atomic

from v1.models.browse_page import BrowsePage
from v1.tests.wagtail_pages.helpers import publish_page


class UpdateChartBlockDatesTestCase(TestCase):
        def test_chart_block(self):
            """ Management command correctly updates chart block dates"""
            browse_page = BrowsePage(
                title='Browse Page',
                slug='browse',
            )

            # Adds a Chart Block to a browse page
            browse_page.content = StreamValue(
                browse_page.content.stream_block,
                [atomic.chart_block],
                True
            )
            publish_page(child=browse_page)

            # Call management command to update values
            filename = os.path.join(
                settings.PROJECT_ROOT,
                'v1/tests/fixtures/data_snapshots.json'
            )
            call_command(
                'update_chart_block_dates',
                '--snapshot_file={}'.format(filename)
            )
            response = self.client.get('/browse/')

            # Tests last_updated_projected_data is correct
            self.assertContains(
                response,
                'The most recent data available in this visualization are for June 2017'
            )
            # Tests date_published is correct
            self.assertContains(response, 'August 2017')
