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

    def get_data_snapshots(self):
        """ Gets all data snapshots from browse pages
        Assumes there is a maximum of one data snapshot per page
        """
        snapshots = []
        for page in BrowsePage.objects.all():
            stream_data = page.specific.content.stream_data
            snapshot = filter(
                lambda item: item['type'] == 'data_snapshot',
                stream_data
            )
            if snapshot:
                snapshot[0]['value']['page'] = page
                snapshots.append(snapshot[0]['value'])
        return snapshots

    def find_data_snapshot(self, market_key, snapshots):
        """ Look up data snapshot by the provided market key
        Assumes there is one data snapshot per key
        """
        for snapshot in snapshots:
            if snapshot['market_key'] == market_key:
                return snapshot

    def handle(self, *args, **options):
        # Read markets from file into update dicts
        with open(self.expand_path(options['snapshot_file'])) as json_data:
            data = json.load(json_data)

        markets = data['markets']
        snapshots = self.get_data_snapshots()
        for market in markets:
            key = market['market_key']
            snapshot = self.find_data_snapshot(key, snapshots)
            if not snapshot:  # Market may not have been added to Wagtail yet
                logger.warn('Market key {} not found'.format(key))
                continue

            # Update snapshot fields with the provided values
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

            # Update denial index info if it exists for this market
            if "denial_yoy_change" in market:
                snapshot['denial_month'] = market['denial_month']
                snapshot['denial_year_over_year_change'] = \
                    market['denial_yoy_change']
            else:
                snapshot['denial_month'] = ""
                snapshot['denial_year_over_year_change'] = ""

            # Publish changes to the browse page the data snapshot lives on
            page = snapshot['page']
            publish_changes(page.specific)
