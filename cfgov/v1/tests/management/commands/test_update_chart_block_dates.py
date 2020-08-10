import json
import os

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase

from wagtail.core.blocks import StreamValue

from scripts import _atomic_helpers as atomic
from v1.management.commands.update_chart_block_dates import get_inquiry_month
from v1.models.browse_page import BrowsePage
from v1.tests.wagtail_pages.helpers import publish_page


class UpdateChartBlockDatesTestCase(TestCase):
        def test_get_inquiry_month(self):
            with open('./v1/tests/fixtures/data_snapshot.json') as json_data:
                data = json.load(json_data)
            markets = data['markets']
            data_source_crc = 'consumer-credit-trends/credit-cards/inq_data_CRC.csv'
            data_source_mtg = 'consumer-credit-trends/mortgages/crt_data_MTG.csv'
            data_source_other = 'consumer-credit-trends/student-loans/num_data_STU.csv'
            
            self.assertEqual(get_inquiry_month(markets, data_source_crc), '2018-06-01')
            self.assertNotEqual(get_inquiry_month(markets, data_source_crc), '2018-02-01')
            self.assertEqual(get_inquiry_month(markets, data_source_mtg), '2017-09-01')
            self.assertNotEqual(get_inquiry_month(markets, data_source_mtg), '2018-06-01')
            self.assertNotEqual(get_inquiry_month(markets, data_source_other), '2018-06-01')
            self.assertIs(get_inquiry_month(markets, data_source_other), None)

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
                'v1/tests/fixtures/data_snapshot.json'
            )
            call_command(
                'update_chart_block_dates',
                '--snapshot_file={}'.format(filename)
            )
            response = self.client.get('/browse/')

            # Tests last_updated_projected_data is correct
            self.assertContains(
                response,
                'The most recent data available in this visualization are for July 2018'
            )

            # Tests date_published is correct
            self.assertContains(response, 'October 2018')

        def test_chart_block_inquiry_activity(self):
            """ Management command correctly updates chart block dates for inquiry index charts"""
            browse_page = BrowsePage(
                title='Browse Page',
                slug='browse',
            )

            # Adds a Chart Block to a browse page
            browse_page.content = StreamValue(
                browse_page.content.stream_block,
                [atomic.chart_block_inquiry_activity],
                True
            )
            publish_page(child=browse_page)

            # Call management command to update values
            filename = os.path.join(
                settings.PROJECT_ROOT,
                'v1/tests/fixtures/data_snapshot.json'
            )
            call_command(
                'update_chart_block_dates',
                '--snapshot_file={}'.format(filename)
            )
            response = self.client.get('/browse/')

            # Tests last_updated_projected_data is correct
            self.assertContains(
                response,
                'The most recent data available in this visualization are for June 2018'
            )

            # Tests date_published is correct
            self.assertContains(response, 'October 2018')

        def test_chart_block_credit_tightness(self):
            """ Management command correctly updates chart block dates for credit tightness charts"""
            browse_page = BrowsePage(
                title='Browse Page',
                slug='browse',
            )

            # Adds a Chart Block to a browse page
            browse_page.content = StreamValue(
                browse_page.content.stream_block,
                [atomic.chart_block_credit_tightness],
                True
            )
            publish_page(child=browse_page)

            # Call management command to update values
            filename = os.path.join(
                settings.PROJECT_ROOT,
                'v1/tests/fixtures/data_snapshot.json'
            )
            call_command(
                'update_chart_block_dates',
                '--snapshot_file={}'.format(filename)
            )
            response = self.client.get('/browse/')

            # Tests last_updated_projected_data is correct
            self.assertContains(
                response,
                'The most recent data available in this visualization are for February 2018'
            )

            # Tests date_published is correct
            self.assertContains(response, 'October 2018')
