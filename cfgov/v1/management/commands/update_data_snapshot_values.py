import json
import logging
import os

from django.core.management.base import BaseCommand

from v1.models.browse_page import BrowsePage
from v1.tests.wagtail_pages.helpers import publish_changes
from v1.util.migrations import set_stream_data


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Monthly updates to data snapshot values'

    def expand_path(self, path):
        """Expand a relative path into an absolute path."""
        rootpath = os.path.abspath(os.path.expanduser(path))

        return rootpath

    def add_arguments(self, parser):
        """Add all arguments to be processed."""
        parser.add_argument(
            '--snapshot_file',
            required=True,
            help='JSON file containing all markets\' data snapshot values'
        )

    def get_data_snapshots(self):
        """
        Get all data snapshots from browse pages.

        Assumes there is a maximum of one data snapshot per page.
        """
        snapshots = []
        for page in BrowsePage.objects.all():
            stream_data = page.content.stream_data
            if stream_data and stream_data[0]['type'] == 'data_snapshot':
                stream_data[0]['value']['page'] = page.pk
                snapshots.append(stream_data)
        return snapshots

    def find_data_snapshot(self, market_key, snapshots):
        """
        Look up data snapshot by the provided market key.

        Assumes there is one data snapshot per key.
        """
        for snapshot in snapshots:
            if snapshot[0]['value']['market_key'] == market_key:
                return snapshot

    def handle(self, *args, **options):
        """Read markets from file into update dicts."""
        with open(self.expand_path(options['snapshot_file'])) as json_data:
            data = json.load(json_data)
        markets = data['markets']
        snapshots = self.get_data_snapshots()
        for market in markets:
            key = market['market_key']
            snapshot_stream_data = self.find_data_snapshot(key, snapshots)
            if not snapshot_stream_data:  # Market may not have been added to Wagtail yet  # noqa
                logger.warning('Market key {} not found'.format(key))
                continue

            # Update snapshot fields with the provided values
            snapshot = snapshot_stream_data[0]['value']
            snapshot['last_updated_projected_data'] = market['data_month']
            snapshot['num_originations'] = market['num_originations']
            snapshot['value_originations'] = market['value_originations']
            snapshot['year_over_year_change'] = market['year_over_year_change']

            # Update inquiry index info if it exists for this market
            if "inquiry_yoy_change" in market:
                snapshot['inquiry_month'] = market['inquiry_month']
                snapshot['inquiry_year_over_year_change'] = \
                    market['inquiry_yoy_change']
            else:
                snapshot['inquiry_month'] = ""
                snapshot['inquiry_year_over_year_change'] = ""

            # Update tightness index info if it exists for this market
            if "tightness_yoy_change" in market:
                snapshot['tightness_month'] = market['tightness_month']
                snapshot['tightness_year_over_year_change'] = \
                    market['tightness_yoy_change']
            else:
                snapshot['tightness_month'] = ""
                snapshot['tightness_year_over_year_change'] = ""

            # Publish changes to the browse page the data snapshot lives on
            page = BrowsePage.objects.get(pk=snapshot['page'])
            del snapshot['page']
            set_stream_data(page, 'content', snapshot_stream_data)
            publish_changes(page)
