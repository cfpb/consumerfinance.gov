import os

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase

from wagtail.core.blocks import StreamValue

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
                'v1/tests/fixtures/data_snapshot.json'
            )
            call_command(
                'update_data_snapshot_values',
                '--snapshot_file={}'.format(filename)
            )
            response = self.client.get('/browse/')

            # July 2018 data:
            self.assertContains(response, '917,007') # Student loans originated
            self.assertContains(response, '$16.6 billion') # Dollar volume of new loans
            self.assertContains(response, '48.0% increase') # In year-over-year originations
            self.assertContains(response, 'July&nbsp;2018')
            self.assertContains(response, 'Loans originated')
            self.assertContains(response, 'Dollar value of new loans')
            self.assertContains(response, 'In year-over-year originations')
            # Should not contain inquiry and tightness values
            self.assertNotContains(response, 'In year-over-year inquiries')
            self.assertNotContains(
                response,
                'In year-over-year credit tightness'
            )

        def test_data_snapshot_with_inquiry_and_tightness(self):
            """ Management command correctly updates data snapshot values
            for market that contains inquiry and tightness data"""
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
                'v1/tests/fixtures/data_snapshot.json'
            )
            call_command(
                'update_data_snapshot_values',
                '--snapshot_file={}'.format(filename)
            )
            # July 2018 
            response = self.client.get('/browse/')
            self.assertContains(response, '2.5 million') # Auto loans originated
            self.assertContains(response, '$54.6 billion') # Dollar volume of new loans
            self.assertContains(response, '7.3% increase') # In year-over-year originations 
            self.assertContains(response, 'July&nbsp;2018')
            self.assertContains(response, 'Loans originated')
            self.assertContains(response, 'Dollar value of new loans')
            self.assertContains(response, 'In year-over-year originations')
            # Inquiry and tightness values
            self.assertContains(response, '7.9% increase')
            self.assertContains(response, '2.8% increase')
            self.assertContains(response, 'In year-over-year inquiries')
            self.assertContains(
                response,
                'In year-over-year credit tightness'
            )
