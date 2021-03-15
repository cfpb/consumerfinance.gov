import json
import logging
import os

from django.core.management.base import BaseCommand

import wagtail

from v1.models.browse_page import BrowsePage
from v1.tests.wagtail_pages.helpers import publish_changes


logger = logging.getLogger(__name__)


def get_inquiry_month(data, data_source):
    for item in data:
        month = None
        if item['market_key'] in data_source:
            if 'inq_' in data_source:
                month = item['inquiry_month']
                break
            elif 'crt_' in data_source:
                month = item['tightness_month']
                break
    return month


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

        for page in BrowsePage.objects.all():
            if wagtail.VERSION < (2, 12):  # pragma: no cover
                data = page.specific.content.stream_data
            else:
                data = page.specific.content.raw_data
            chart_blocks = filter(
                lambda item: item['type'] == 'chart_block',
                data
            )
            if not chart_blocks:
                continue
            for chart in chart_blocks:
                chart_options = chart['value']
                chart['value']['date_published'] = date_published
                if chart_options['chart_type'] == 'line-index':
                    last_updated_inquiry = get_inquiry_month(
                        markets, chart_options['data_source']
                    )
                    chart['value']['last_updated_projected_data'] = \
                        last_updated_inquiry
                else:
                    chart['value']['last_updated_projected_data'] = \
                        last_updated
            publish_changes(page.specific)

    def handle(self, *args, **options):
        # Read in CCT snapshot data from json file
        with open(self.expand_path(options['snapshot_file'])) as json_data:
            data = json.load(json_data)

        markets = data['markets']
        date_published = data['date_published']
        last_updated = max(
            [item['data_month'] for item in markets]
        )
        inquiry_activity_charts = \
            [item for item in markets if 'inquiry_month' in item]

        self.update_chart_blocks(
            date_published, last_updated, inquiry_activity_charts
        )
