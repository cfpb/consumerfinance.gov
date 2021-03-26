import datetime
import re

from django.test import TestCase
from django.test.utils import override_settings

import pytz
import responses
from freezegun import freeze_time

from v1.models import EventPage
from v1.tests.wagtail_pages.helpers import save_new_page


class EventPageTests(TestCase):
    @override_settings(MAPBOX_ACCESS_TOKEN='test_token')
    @responses.activate
    def test_save_calls_get_venue_coords(self):
        api_url_re = re.compile('https://api.mapbox.com/geocoding/(.*)')
        data_json = {
            'features': [{
                'geometry': {
                    'coordinates': [
                        '123.456',
                        '321.654'
                    ]
                }
            }]
        }
        responses.add(responses.GET, api_url_re, json=data_json)

        page = EventPage(
            title='Super fun event',
            start_dt=datetime.datetime.now(pytz.UTC),
            venue_city='Boston',
            venue_state='MA'
        )
        save_new_page(page)
        self.assertEqual(page.venue_coords, '123.456,321.654')
        self.assertIn('static/123.456,321.654', page.location_image_url())

    def test_venue_coords_without_saving(self):
        page = EventPage(title='Party time')
        # Should get static image URL even if page hasn't been saved
        self.assertIn('static/-77.039628,38.898238', page.location_image_url())

    @freeze_time('2011-01-03')
    def test_present_event_with_livestream_includes_video_js(self):
        page = EventPage(
            title='Present event with live_stream_date',
            start_dt=datetime.datetime(2011, 1, 2, tzinfo=pytz.UTC),
            end_dt=datetime.datetime(2011, 1, 4, tzinfo=pytz.UTC),
            live_stream_date=datetime.datetime(2011, 1, 2, tzinfo=pytz.UTC)
        )
        save_new_page(page)
        self.assertEqual('present', page.event_state)
        self.assertIn('video-player.js', page.page_js)

    @freeze_time('2011-01-03')
    def test_past_event_with_video_includes_video_js(self):
        page = EventPage(
            title='Past event with archive_video_id',
            start_dt=datetime.datetime(2011, 1, 1, tzinfo=pytz.UTC),
            end_dt=datetime.datetime(2011, 1, 2, tzinfo=pytz.UTC),
            archive_video_id='Aa1Bb2Cc3Dc'
        )
        save_new_page(page)
        self.assertEqual('past', page.event_state)
        self.assertIn('video-player.js', page.page_js)

    @freeze_time('2011-01-03')
    def test_video_js_not_included_on_event_when_not_needed(self):
        page = EventPage(
            title='Future event with no end date',
            start_dt=datetime.datetime(2011, 1, 4, tzinfo=pytz.UTC)
        )
        save_new_page(page)
        self.assertEqual('future', page.event_state)
        self.assertNotIn('video-player.js', page.page_js)

        page = EventPage(
            title='Future event with end date',
            start_dt=datetime.datetime(2011, 1, 4, tzinfo=pytz.UTC),
            end_dt=datetime.datetime(2011, 1, 5, tzinfo=pytz.UTC)
        )
        save_new_page(page)
        self.assertEqual('future', page.event_state)
        self.assertNotIn('video-player.js', page.page_js)

        page = EventPage(
            title='Present event with no live_stream_date',
            start_dt=datetime.datetime(2011, 1, 2, tzinfo=pytz.UTC),
            end_dt=datetime.datetime(2011, 1, 4, tzinfo=pytz.UTC)
        )
        save_new_page(page)
        self.assertEqual('present', page.event_state)
        self.assertNotIn('video-player.js', page.page_js)

        page = EventPage(
            title='Past event with no archive_video_id',
            start_dt=datetime.datetime(2011, 1, 1, tzinfo=pytz.UTC),
            end_dt=datetime.datetime(2011, 1, 2, tzinfo=pytz.UTC)
        )
        save_new_page(page)
        self.assertEqual('past', page.event_state)
        self.assertNotIn('video-player.js', page.page_js)
