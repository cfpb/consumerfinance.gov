import mock
from datetime import datetime
from importlib import import_module

from django.apps import apps
from django.test import TestCase

from pytz import timezone

from v1.models import EventPage
from v1.tests.wagtail_pages.helpers import save_new_page


class TestMigration0155(TestCase):
    def setUp(self):
        self.page = EventPage(
            title='Super fun event',
            start_dt=datetime.now(timezone('UTC')),
            venue_city='Boston',
            venue_state='MA'
        )
        save_new_page(self.page)
        self.migration = import_module(
            'v1.migrations.0155_add_venue_coords_to_existing_events'
        )

    @mock.patch(
        'v1.migrations.0155_add_venue_coords_to_existing_events.get_venue_coords'  # noqa
    )
    def test_forwards(self, mock_get_venue_coords):
        mock_get_venue_coords.return_value = '123.456,321.654'
        self.migration.forwards(apps, None)
        mock_get_venue_coords.assert_called_with('Boston', 'MA')
