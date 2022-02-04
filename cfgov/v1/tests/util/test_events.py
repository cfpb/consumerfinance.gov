import re

from django.test import TestCase
from django.test.utils import override_settings

import responses

from v1.util.events import get_venue_coords


class EventUtilTestCase(TestCase):

    def test_get_venue_coords_no_mapbox_token(self):
        # Should default to DC coords if no mapbox token was provided
        self.assertEqual(get_venue_coords(), '-77.039628,38.898238')

    @override_settings(MAPBOX_ACCESS_TOKEN='test_token')
    @responses.activate
    def test_get_venue_coords(self):
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

        coords = get_venue_coords(city='Boston', state='MA')
        self.assertEqual(coords, '123.456,321.654')

    @override_settings(MAPBOX_ACCESS_TOKEN='test_token')
    @responses.activate
    def test_get_venue_coords_broken_api_format(self):
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

        coords = get_venue_coords(city='Boston', state='MA')
        self.assertEqual(coords, '-77.039628,38.898238')

    @override_settings(MAPBOX_ACCESS_TOKEN='test_token')
    def test_get_venue_coords_default_venue_coords(self):
        # Should default to DC coords if no city/state provided
        self.assertEqual(get_venue_coords(), '-77.039628,38.898238')

    @override_settings(MAPBOX_ACCESS_TOKEN='test_token')
    def test_get_venue_coords_default_venue_coords_when_empty(self):
        # Should default to DC coords if no city/state provided
        self.assertEqual(
            get_venue_coords(city='', state=''),
            '-77.039628,38.898238'
        )

    @override_settings(MAPBOX_ACCESS_TOKEN='test_token')
    @responses.activate
    def test_get_venue_coords_bad_http_response(self):
        api_url_re = re.compile('https://api.mapbox.com/geocoding/(.*)')
        responses.add(responses.GET, api_url_re, status=401)

        # Should default to DC coords if API request bombed
        coords = get_venue_coords(city='Boston', state='MA')
        self.assertEqual(coords, '-77.039628,38.898238')

    @override_settings(MAPBOX_ACCESS_TOKEN='test_token')
    @responses.activate
    def test_get_venue_coords_bad_mapbox_response(self):
        api_url_re = re.compile('https://api.mapbox.com/geocoding/(.*)')
        data_json = {'error': 'Failed to find location'}
        responses.add(responses.GET, api_url_re, json=data_json)

        # Should default to DC coords if MapBox returns bad JSON
        self.assertEqual(get_venue_coords(), '-77.039628,38.898238')
