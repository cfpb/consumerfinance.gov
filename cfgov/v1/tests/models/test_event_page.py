import re

from django.test import TestCase
from django.test.utils import override_settings

import responses

from v1.models import EventPage
from v1.tests.wagtail_pages.helpers import save_new_page


class EventPageTests(TestCase):
    def test_no_mapbox_token(self):
        page = EventPage(title='Something is happening', venue_city='Boston', venue_state='MA')
        save_new_page(page)
        # Should default to DC coords if no mapbox token was provided
        self.assertEqual(page.get_venue_coords(), '-77.039628,38.898238')
        self.assertEqual(page.venue_coords, '-77.039628,38.898238')

    @override_settings(MAPBOX_ACCESS_TOKEN='test_token')
    @responses.activate
    def test_venue_coords(self):
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

        page = EventPage(title='Super fun event', venue_city='Boston', venue_state='MA')
        save_new_page(page)
        self.assertEqual(page.get_venue_coords(), '123.456,321.654')
        self.assertEqual(page.venue_coords, '123.456,321.654')
        self.assertIn('static/123.456,321.654', page.location_image_url())

    @override_settings(MAPBOX_ACCESS_TOKEN='test_token')
    @responses.activate
    def test_broken_api_format(self):
        api_url_re = re.compile('https://api.mapbox.com/geocoding/(.*)')
        data_json = {
            'features': [{
                'new_geometry': {
                    'coordinates': [
                        '123.456',
                        '321.654'
                    ]
                }
            }]
        }
        responses.add(responses.GET, api_url_re, json=data_json)

        page = EventPage(title='Fancy event', venue_city='Boston', venue_state='MA')
        save_new_page(page)
        # Should use default coords if Mapbox API introduces breaking change
        self.assertEqual(page.get_venue_coords(), '-77.039628,38.898238')
        self.assertEqual(page.venue_coords, '-77.039628,38.898238')

    @override_settings(MAPBOX_ACCESS_TOKEN='test_token')
    def test_venue_coords_without_saving(self):
        page = EventPage(title='Party time')
        # Should get static image URL even if page wasn't saved
        self.assertIn('static/-77.039628,38.898238', page.location_image_url())

    @override_settings(MAPBOX_ACCESS_TOKEN='test_token')
    def test_default_venue_coords(self):
        page = EventPage(title='Another super fun event')
        save_new_page(page)
        # Should default to DC coords if no city/state provided
        self.assertEqual(page.get_venue_coords(), '-77.039628,38.898238')
        self.assertEqual(page.venue_coords, '-77.039628,38.898238')

    @override_settings(MAPBOX_ACCESS_TOKEN='test_token')
    @responses.activate
    def test_bad_http_response(self):
        api_url_re = re.compile('https://api.mapbox.com/geocoding/(.*)')
        responses.add(responses.GET, api_url_re, status=401)

        page = EventPage(title='Some event', venue_city='Boston', venue_state='MA')
        save_new_page(page)
        # Should default to DC coords if API request bombed
        self.assertEqual(page.get_venue_coords(), '-77.039628,38.898238')
        self.assertEqual(page.venue_coords, '-77.039628,38.898238')

    @override_settings(MAPBOX_ACCESS_TOKEN='test_token')
    @responses.activate
    def test_bad_mapbox_response(self):
        api_url_re = re.compile('https://api.mapbox.com/geocoding/(.*)')
        data_json = {'error': 'Failed to find location'}
        responses.add(responses.GET, api_url_re, json=data_json)

        page = EventPage(title='Yet another super fun event')
        save_new_page(page)
        # Should default to DC coords if MapBox returns bad JSON
        self.assertEqual(page.get_venue_coords(), '-77.039628,38.898238')
        self.assertEqual(page.venue_coords, '-77.039628,38.898238')
