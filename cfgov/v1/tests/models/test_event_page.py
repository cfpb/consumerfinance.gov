import datetime
import re

from django.core.exceptions import ValidationError
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
    def test_future_event_with_start_date(self):
        page = EventPage(
            title='Future event with start date',
            start_dt=datetime.datetime(2011, 1, 5, tzinfo=pytz.UTC)
        )
        save_new_page(page)
        self.assertEqual('future', page.event_state)

        # Should not include video JavaScript.
        self.assertNotIn('video-player.js', page.page_js)

        # Page should send HTTP Expires header for its start time.
        response = self.client.get('/future-event-with-start-date/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Expires'], 'Wed, 05 Jan 2011 00:00:00 GMT')

    @freeze_time('2011-01-03')
    def test_future_event_with_livestream_default_date(self):
        page = EventPage(
            title='Future event with livestream date defaulting to start date',
            start_dt=datetime.datetime(2011, 1, 5, tzinfo=pytz.UTC),
            live_stream_availability=True
        )
        save_new_page(page)
        self.assertEqual(page.start_dt, page.live_stream_date)

    @freeze_time('2011-01-03')
    def test_future_event_with_livestream_date(self):
        page = EventPage(
            title='Future event with livestream date',
            start_dt=datetime.datetime(2011, 1, 5, tzinfo=pytz.UTC),
            live_stream_availability=True,
            live_stream_date=datetime.datetime(2011, 1, 4, tzinfo=pytz.UTC)
        )
        save_new_page(page)
        self.assertEqual('future', page.event_state)

        # Should not include video JavaScript.
        self.assertNotIn('video-player.js', page.page_js)

        # Page should send HTTP Expires header for its live stream time,
        # because it comes before the start time.
        response = self.client.get('/future-event-with-livestream-date/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Expires'], 'Tue, 04 Jan 2011 00:00:00 GMT')

    @freeze_time('2011-01-03')
    def test_present_event_with_livestream_and_end_date(self):
        page = EventPage(
            title='Present event with livestream',
            start_dt=datetime.datetime(2011, 1, 2, tzinfo=pytz.UTC),
            live_stream_availability=True,
            live_stream_date=datetime.datetime(2011, 1, 2, tzinfo=pytz.UTC),
            end_dt=datetime.datetime(2011, 1, 4, tzinfo=pytz.UTC)
        )
        save_new_page(page)
        self.assertEqual('present', page.event_state)

        # Should include video JavaScript.
        self.assertIn('video-player.js', page.page_js)

        # Page should send HTTP Expires header for its end time.
        response = self.client.get('/present-event-with-livestream/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Expires'], 'Tue, 04 Jan 2011 00:00:00 GMT')

    @freeze_time('2011-01-03')
    def test_present_event_without_livestream_or_end_date(self):
        page = EventPage(
            title='Present event without livestream',
            start_dt=datetime.datetime(2011, 1, 2, tzinfo=pytz.UTC)
        )
        save_new_page(page)
        self.assertEqual('present', page.event_state)

        # Should not include video JavaScript without livestream.
        self.assertNotIn('video-player.js', page.page_js)

        # Page should not send HTTP Expires header.
        response = self.client.get('/present-event-without-livestream/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('Expires', response)

    @freeze_time('2011-01-03')
    def test_past_event_with_video(self):
        page = EventPage(
            title='Past event with video',
            start_dt=datetime.datetime(2011, 1, 1, tzinfo=pytz.UTC),
            end_dt=datetime.datetime(2011, 1, 2, tzinfo=pytz.UTC),
            archive_video_id='Aa1Bb2Cc3Dc'
        )
        save_new_page(page)
        self.assertEqual('past', page.event_state)

        # Should include video JavaScript.
        self.assertIn('video-player.js', page.page_js)

        # Page should not send HTTP Expires header.
        response = self.client.get('/past-event-with-video/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('Expires', response)

    @freeze_time('2011-01-03')
    def test_past_event_without_video(self):
        page = EventPage(
            title='Past event without video',
            start_dt=datetime.datetime(2011, 1, 1, tzinfo=pytz.UTC),
            end_dt=datetime.datetime(2011, 1, 2, tzinfo=pytz.UTC)
        )
        save_new_page(page)
        self.assertEqual('past', page.event_state)
        self.assertNotIn('video-player.js', page.page_js)

        # Page should not send HTTP Expires header.
        response = self.client.get('/past-event-without-video/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('Expires', response)

    def assertValidationFails(self, expected_msg, **kwargs):
        page = EventPage(
            title='test',
            start_dt=datetime.datetime.now(pytz.UTC),
            **kwargs
        )

        with self.assertRaisesRegex(ValidationError, expected_msg):
            save_new_page(page)

    def test_failing_validation_venue_image(self):
        self.assertValidationFails(
            'Required if "Venue image type" is "Image".',
            venue_image_type='image'
        )

    def test_failing_validation_post_event_image(self):
        self.assertValidationFails(
            'Required if "Post-event image type" is "Image".',
            post_event_image_type='image'
        )

    def test_failing_validation_live_start_date(self):
        self.assertValidationFails(
            'Cannot be on or after Event End.',
            end_dt=datetime.datetime.now(pytz.UTC) +
            datetime.timedelta(hours=1),
            live_stream_availability=True,
            live_stream_date=datetime.datetime.now(pytz.UTC) +
            datetime.timedelta(hours=2)
        )
