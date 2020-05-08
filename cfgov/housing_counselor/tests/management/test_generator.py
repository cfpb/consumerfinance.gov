import json
import os
import shutil
import tempfile
from unittest import TestCase

from housing_counselor.generator import (
    distance_in_miles, generate_counselor_json, get_counselor_json_files
)


class TestDistanceInMiles(TestCase):
    def test_zero_distance(self):
        latitude = 0.5
        longitude = 0.3

        self.assertEqual(
            distance_in_miles(latitude, longitude, latitude, longitude),
            0
        )


class TestGeneratorCounselorJson(TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()

        self.counselors = [
            {'agc_ADDR_LATITUDE': 120, 'agc_ADDR_LONGITUDE': 98},
            {'agc_ADDR_LATITUDE': 125, 'agc_ADDR_LONGITUDE': 99},
        ]

        self.zipcodes = {
            '20001': (115.5, 97.5),
            '20002': (130.3, 100.1),
        }

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def test_generate_creates_json_files(self):
        generate_counselor_json(self.counselors, self.zipcodes, self.tempdir)
        self.assertCountEqual(
            os.listdir(self.tempdir),  # os.listdir order not guaranteed.
            ['20001.json', '20002.json']
        )

    def test_generate_creates_proper_json(self):
        generate_counselor_json(self.counselors, self.zipcodes, self.tempdir)
        with open(os.path.join(self.tempdir, '20001.json')) as f:
            data = json.load(f)

        self.assertEqual(data['zip'], {
            'lat': 115.5,
            'lng': 97.5,
            'zipcode': '20001',
        })

        agencies = data['counseling_agencies']
        self.assertEqual(len(agencies), 2)

        expected_agencies = [
            {
                'agc_ADDR_LATITUDE': 120,
                'agc_ADDR_LONGITUDE': 98,
                'distance': 311.35243783709234,
            },
            {
                'agc_ADDR_LATITUDE': 125,
                'agc_ADDR_LONGITUDE': 99,
                'distance': 658.4536705140896,
            },
        ]

        for a, b in zip(agencies, expected_agencies):
            self.assertCountEqual(a.keys(), b.keys())

            for k in a:
                self.assertAlmostEqual(a[k], b[k])


class TestGetCounselorJsonFiles(TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def make_empty_file(self, filename):
        open(os.path.join(self.tempdir, filename), 'w').close()

    def test_no_files_raises_runtime_error(self):
        with self.assertRaises(RuntimeError):
            list(get_counselor_json_files(self.tempdir))

    def test_no_matching_files_raises_runtime_error(self):
        self.make_empty_file('something.json')
        with self.assertRaises(RuntimeError):
            list(get_counselor_json_files(self.tempdir))

    def test_matching_files_returns_zipcodes_and_filenames(self):
        self.make_empty_file('20001.json')
        self.make_empty_file('20002.json')
        self.make_empty_file('something.json')

        self.assertEqual(
            sorted(list(get_counselor_json_files(self.tempdir))),
            sorted([
                ('20001', os.path.join(self.tempdir, '20001.json')),
                ('20002', os.path.join(self.tempdir, '20002.json')),
            ])
        )
