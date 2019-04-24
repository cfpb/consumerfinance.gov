import re
import responses

from django.test import TestCase
from django.test.utils import override_settings

from v1.models import EventPage
from v1.tests.wagtail_pages.helpers import save_new_page

class EventPageTests(TestCase):
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
    def test_default_venue_coords(self):
        page = EventPage(title='Another super fun event')
        save_new_page(page)
        # Should default to DC coords if no city/state provided
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
