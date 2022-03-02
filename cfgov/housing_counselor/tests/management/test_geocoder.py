from unittest import TestCase
from unittest.mock import patch

from housing_counselor.geocoder import (
    BulkZipCodeGeocoder,
    ZipCodeBasedCounselorGeocoder,
    geocode_counselors,
)


class TestGeocodeCounselors(TestCase):
    def test_calls_zipcode_based_geocoder_and_passes_zipcodes(self):
        zipcodes = object()
        cls = "housing_counselor.geocoder.ZipCodeBasedCounselorGeocoder"
        with patch(cls) as p:
            geocode_counselors([], zipcodes=zipcodes)
            p.assert_called_once_with(zipcodes=zipcodes)


class TestZipCodeBasedCounselorGeocoder(TestCase):
    def setUp(self):
        self.zipcodes = {
            "20001": (123.45, -78.9),
        }
        self.geocoder = ZipCodeBasedCounselorGeocoder(self.zipcodes)

    def test_returns_list_of_counselors(self):
        counselors = [
            {"agc_ADDR_LATITUDE": 1, "agc_ADDR_LONGITUDE": -1},
            {"agc_ADDR_LATITUDE": 2, "agc_ADDR_LONGITUDE": -2},
            {"agc_ADDR_LATITUDE": 3, "agc_ADDR_LONGITUDE": -3},
        ]

        geocoded = self.geocoder.geocode(counselors)
        self.assertEqual(len(geocoded), 3)

    def test_leaves_existing_lat_lng_alone(self):
        counselor = {
            "agc_ADDR_LATITUDE": 99.9,
            "agc_ADDR_LONGITUDE": 88.8,
            "zipcd": "20001",
        }

        geocoded = self.geocoder.geocode([counselor])
        self.assertEqual(geocoded[0]["agc_ADDR_LATITUDE"], 99.9)
        self.assertEqual(geocoded[0]["agc_ADDR_LONGITUDE"], 88.8)

    def check_uses_zipcodes(self, counselor):
        geocoded = self.geocoder.geocode([counselor])
        self.assertEqual(geocoded[0]["agc_ADDR_LATITUDE"], 123.45)
        self.assertEqual(geocoded[0]["agc_ADDR_LONGITUDE"], -78.9)

    def test_uses_zipcodes_if_lat_lng_not_present(self):
        self.check_uses_zipcodes(
            {
                "zipcd": "20001",
            }
        )

    def test_uses_zipcodes_if_lat_lng_is_zero_integer(self):
        self.check_uses_zipcodes(
            {
                "agc_ADDR_LATITUDE": 0,
                "agc_ADDR_LONGITUDE": 0,
                "zipcd": "20001",
            }
        )

    def test_uses_zipcodes_if_lat_lng_is_zero_float(self):
        self.check_uses_zipcodes(
            {
                "agc_ADDR_LATITUDE": 0.0,
                "agc_ADDR_LONGITUDE": 0.0,
                "zipcd": "20001",
            }
        )

    def test_uses_first_five_digits_of_zipcode(self):
        counselor = {
            "zipcd": "20001-1234",
        }

        geocoded = self.geocoder.geocode([counselor])
        self.assertEqual(geocoded[0]["agc_ADDR_LATITUDE"], 123.45)
        self.assertEqual(geocoded[0]["agc_ADDR_LONGITUDE"], -78.9)

    def test_raises_keyerror_if_zipcode_not_available(self):
        counselor = {"zipcd": "20002"}

        with self.assertRaises(KeyError):
            self.geocoder.geocode([counselor])


class TestBulkZipCodeGeocoder(TestCase):
    def test_chunker_empty_list(self):
        self.assertEqual(list(BulkZipCodeGeocoder.chunker([], 3)), [])

    def test_chunker_less_than_one_chunk(self):
        self.assertEqual(
            list(BulkZipCodeGeocoder.chunker([1, 2], 3)), [(1, 2)]
        )

    def test_chunker_elements_fit_exactly_into_chunks(self):
        self.assertEqual(
            list(BulkZipCodeGeocoder.chunker([1, 2, 3, 4, 5, 6], 3)),
            [(1, 2, 3), (4, 5, 6)],
        )

    def test_chunker_elements_do_not_fit_exactly_into_chunks(self):
        self.assertEqual(
            list(BulkZipCodeGeocoder.chunker([1, 2, 3, 4, 5], 3)),
            [(1, 2, 3), (4, 5)],
        )

    def test_generate_possible_zipcodes(self):
        zipcodes = list(BulkZipCodeGeocoder.generate_possible_zipcodes())
        self.assertEqual(len(zipcodes), 100000)
        self.assertEqual(zipcodes[1234], "01234")
        self.assertEqual(zipcodes[98765], "98765")

    def test_generate_possible_zipcodes_partial(self):
        zipcodes = list(BulkZipCodeGeocoder.generate_possible_zipcodes(1234))
        self.assertEqual(len(zipcodes), 98766)
        self.assertEqual(zipcodes[0], "01234")
        self.assertEqual(zipcodes[-1], "99999")
