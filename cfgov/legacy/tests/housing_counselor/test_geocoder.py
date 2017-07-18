from mock import patch
from unittest import TestCase

from legacy.housing_counselor.geocoder import (
    ZipCodeBasedGeocoder, geocode_counselors
)


class TestGeocodeCounselors(TestCase):
    def test_calls_zipcode_based_geocoder_and_passes_zipcodes(self):
        zipcodes = object()
        cls = 'legacy.housing_counselor.geocoder.ZipCodeBasedGeocoder'
        with patch(cls) as p:
            geocode_counselors([], zipcodes=zipcodes)
            p.assert_called_once_with(zipcodes=zipcodes)


class TestZipCodeBasedGeocoder(TestCase):
    def setUp(self):
        self.zipcodes = {
            '20001': (123.45, -78.9),
        }
        self.geocoder = ZipCodeBasedGeocoder(self.zipcodes)

    def test_returns_list_of_counselors(self):
        counselors = [
            {'agc_ADDR_LATITUDE': 1, 'agc_ADDR_LONGITUDE': -1},
            {'agc_ADDR_LATITUDE': 2, 'agc_ADDR_LONGITUDE': -2},
            {'agc_ADDR_LATITUDE': 3, 'agc_ADDR_LONGITUDE': -3},
        ]

        geocoded = self.geocoder.geocode(counselors)
        self.assertEqual(len(geocoded), 3)

    def test_leaves_existing_lat_lng_alone(self):
        counselor = {
            'agc_ADDR_LATITUDE': 99.9,
            'agc_ADDR_LONGITUDE': 88.8,
            'zipcd': '20001',
        }

        geocoded = self.geocoder.geocode([counselor])
        self.assertEqual(geocoded[0]['agc_ADDR_LATITUDE'], 99.9)
        self.assertEqual(geocoded[0]['agc_ADDR_LONGITUDE'], 88.8)

    def check_uses_zipcodes(self, counselor):
        geocoded = self.geocoder.geocode([counselor])
        self.assertEqual(geocoded[0]['agc_ADDR_LATITUDE'], 123.45)
        self.assertEqual(geocoded[0]['agc_ADDR_LONGITUDE'], -78.9)

    def test_uses_zipcodes_if_lat_lng_not_present(self):
        self.check_uses_zipcodes({
            'zipcd': '20001',
        })

    def test_uses_zipcodes_if_lat_lng_is_zero_integer(self):
        self.check_uses_zipcodes({
            'agc_ADDR_LATITUDE': 0,
            'agc_ADDR_LONGITUDE': 0,
            'zipcd': '20001',
        })

    def test_uses_zipcodes_if_lat_lng_is_zero_float(self):
        self.check_uses_zipcodes({
            'agc_ADDR_LATITUDE': 0.0,
            'agc_ADDR_LONGITUDE': 0.0,
            'zipcd': '20001',
        })

    def test_uses_first_five_digits_of_zipcode(self):
        counselor = {
            'zipcd': '20001-1234',
        }

        geocoded = self.geocoder.geocode([counselor])
        self.assertEqual(geocoded[0]['agc_ADDR_LATITUDE'], 123.45)
        self.assertEqual(geocoded[0]['agc_ADDR_LONGITUDE'], -78.9)

    def test_raises_keyerror_if_zipcode_not_available(self):
        counselor = {
            'zipcd': '20002'
        }

        with self.assertRaises(KeyError):
            self.geocoder.geocode([counselor])
