import json
import logging
import os

from django.core.management.base import BaseCommand

from v1.models.browse_page import BrowsePage
from v1.tests.wagtail_pages.helpers import publish_changes


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Monthly updates to data snapshot values'

    def expand_path(self, path):
        """Expands a relative path into an absolute path"""
        rootpath = os.path.abspath(os.path.expanduser(path))

        return rootpath

    def add_arguments(self, parser):
        """Adds all arguments to be processed."""
        parser.add_argument(
            '--snapshot_file',
            required=True,
            help='JSON file containing all markets\' data snapshot values'
        )

    def update_chart_blocks(self, date_published, last_updated, markets):
        """ Update date_published on all chart blocks """

        # check if market key is in the data source string - if so it's the correct market
        def is_market(data, market):
            for item in data:
                market_key = item['market_key']
                if market_key in market:
                    # end and exit loop and return true
                    print item['market_key'] + market
                    break
                return True
            else:
                return False

        def get_inquiry_month(data, market):
            for item in data:
                # print item['inquiry_month']
                # nested loops with the is_market call
                # if inquiry month or tightness month keys are in the data, then it is an line index data
                # then need to check if it's tightness chart or inquiry index chart (based on data source)
                # THEN get the value for the correct market
                # if it's not the right market then we continue the loop
                if 'inquiry_month' in item:
                    month = item['inquiry_month'] if is_market(data, market) else '2020-02-02'
                # elif 'tightness_month' in item  AND chart source is credit tightness, then get the value for the correct market's tightness
                else:
                    month = '2025-02-02'
            return month

        for page in BrowsePage.objects.all():
            chart_blocks = filter(
                lambda item: item['type'] == 'chart_block',
                page.specific.content.stream_data
            )
            if not chart_blocks:
                continue
            for chart in chart_blocks:
                chart['value']['date_published'] = date_published
                # use tightness_month for credit tightness charts
                # use inquiry_month for inquiry index charts
                if chart['value']['chart_type'] == 'line-index':
                    last_updated_inquiry = get_inquiry_month(markets, chart['value']['data_source'])
                    chart['value']['last_updated_projected_data'] = last_updated_inquiry
                else:
                    chart['value']['last_updated_projected_data'] = last_updated
            publish_changes(page.specific)

    def handle(self, *args, **options):
        # Read in CCT snapshot data from json file
        with open(self.expand_path(options['snapshot_file'])) as json_data:
            data = json.load(json_data)

        date_published = data['date_published']
        last_updated = max(
            [item['data_month'] for item in data['markets']]
        )

        markets = data['markets']

        self.update_chart_blocks(date_published, last_updated, markets)
