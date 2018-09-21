import os

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase

from wagtail.wagtailcore.blocks import StreamValue

from scripts import _atomic_helpers as atomic

from v1.models.browse_page import BrowsePage
from v1.tests.wagtail_pages.helpers import publish_page


class UpdateDataSnapshotValuesTestCase(TestCase):
        def test_data_snapshot(self):
            """ Management command correctly updates data snapshot values"""
            browse_page = BrowsePage(
                title='Browse Page',
                slug='browse',
            )

            # Adds a STU market to a browse page
            browse_page.content = StreamValue(
                browse_page.content.stream_block,
                [atomic.data_snapshot],
                True
            )
            publish_page(child=browse_page)

            # Call management command to update values
            filename = os.path.join(
                settings.PROJECT_ROOT,
                'v1/tests/fixtures/data_snapshots.json'
            )
            call_command(
                'update_data_snapshot_values',
                '--snapshot_file={}'.format(filename)
            )
            response = self.client.get('/browse/')
            self.assertContains(response, '458,407')
            self.assertContains(response, '$8.0 billion')
            self.assertContains(response, '32.6% increase')
            self.assertContains(response, 'March&nbsp;2017')
            self.assertContains(response, 'Loans originated')
            self.assertContains(response, 'Dollar value of new loans')
            self.assertContains(response, 'In year-over-year originations')
            # Should not contain inquiry and denial values
            self.assertNotContains(response, '3.2% increase')
            self.assertNotContains(response, '7.0% increase')
            self.assertNotContains(response, 'In year-over-year inquiries')
            self.assertNotContains(
                response,
                'In year-over-year credit tightness'
            )

        def test_data_snapshot_with_inquiry_and_denial(self):
            """ Management command correctly updates data snapshot values
            for market that contains inquiry and denial data"""
            browse_page = BrowsePage(
                title='Browse Page',
                slug='browse',
            )

            # Adds a AUT market to a browse page
            browse_page.content = StreamValue(
                browse_page.content.stream_block,
                [atomic.data_snapshot_with_optional_fields],
                True
            )
            publish_page(child=browse_page)

            # Call management command to update values
            filename = os.path.join(
                settings.PROJECT_ROOT,
                'v1/tests/fixtures/data_snapshots.json'
            )
            call_command(
                'update_data_snapshot_values',
                '--snapshot_file={}'.format(filename)
            )
            response = self.client.get('/browse/')
            self.assertContains(response, '2.1 million')
            self.assertContains(response, '$46.4 billion')
            self.assertContains(response, '5.8% increase')
            self.assertContains(response, 'March&nbsp;2017')
            self.assertContains(response, 'Loans originated')
            self.assertContains(response, 'Dollar value of new loans')
            self.assertContains(response, 'In year-over-year originations')
            # Inquiry and denial values
            self.assertContains(response, '3.2% increase')
            self.assertContains(response, '7.0% increase')
            self.assertContains(response, 'In year-over-year inquiries')
            self.assertContains(
                response,
                'In year-over-year credit tightness'
            )
