from __future__ import unicode_literals

import mock
import unittest

import django.test

from data_research.scripts.load_mortgage_performance_csv import (
    CountyMortgageData,
    validate_fips,
    read_in_s3,
    load_values,
    run as run_csv_loader
)
from data_research.scripts.load_aggregates import (
    run as run_aggregates,
    load_msa_values
)
from data_research.views import FIPS, load_dates


class AggregateLoadTest(django.test.TestCase):
    """Tests aggregate loading function"""

    def setUp(self):
        print_patch = mock.patch(
            'data_research.scripts.load_aggregates.print'
        )
        print_patch.start()
        self.addCleanup(print_patch.stop)

    def test_load_values(self):
        date = "2016-09-01"
        load_msa_values(date)
        pass


class DataLoadTest(django.test.TestCase):
    """Tests loading functions"""

    def setUp(self):
        print_patch = mock.patch(
            'data_research.scripts.load_mortgage_performance_csv.print'
        )
        print_patch.start()
        self.addCleanup(print_patch.stop)

        print_patch2 = mock.patch(
            'data_research.scripts.load_aggregates.print'
        )
        print_patch2.start()
        self.addCleanup(print_patch2.stop)

    @mock.patch('data_research.scripts.'
                'load_mortgage_performance_csv.read_in_s3')
    def test_load_values(self, mock_read_in):
        mock_read_in.return_value = [{
            'thirty': '4', 'month': '1', 'current': '262', 'sixty': '1',
            'ninety': '0', 'date': '01/01/98', 'open': '270', 'other': '3',
            'fipstop': '01001'}]
        load_values()
        self.assertEqual(mock_read_in.call_count, 1)
        self.assertEqual(CountyMortgageData.objects.count(), 1)


class DataScriptTest(unittest.TestCase):
    """Tests for data pipeline automations"""

    def setUp(self):
        print_patch = mock.patch(
            'data_research.scripts.load_mortgage_performance_csv.print'
        )
        print_patch.start()
        self.addCleanup(print_patch.stop)

        print_patch2 = mock.patch(
            'data_research.scripts.load_aggregates.print'
        )
        print_patch2.start()
        self.addCleanup(print_patch2.stop)

    def test_validate_fips_too_short(self):
        fips_input = '12'
        self.assertEqual(validate_fips(fips_input), None)

    def test_validate_fips_too_long(self):
        fips_input = '123456'
        self.assertEqual(validate_fips(fips_input), None)

    def test_validate_fips_edge_case(self):
        fips_input = '46113'
        self.assertEqual(validate_fips(fips_input), '46102')

    def test_validate_fips_4_digit(self):
        fips_input = '1015'
        self.assertEqual(validate_fips(fips_input), '01015')

    def test_validate_fips_invalid_5_digit(self):
        fips_input = '02201'
        self.assertEqual(validate_fips(fips_input), None)

    def test_validate_fips_valid_5_digit(self):
        fips_input = '34041'
        self.assertEqual(validate_fips(fips_input), '34041')

    @mock.patch('data_research.scripts.'
                'load_mortgage_performance_csv.requests.get')
    def test_read_in_s3(self, mock_requests):
        mock_requests.return_value.content = 'a,b,c\nd,e,f'.format('utf-8')
        reader = read_in_s3('fake-s3-url.com')
        self.assertEqual(mock_requests.call_count, 1)
        self.assertEqual(reader.fieldnames, ['a', 'b', 'c'])
        self.assertEqual(sorted(reader.next().values()), ['d', 'e', 'f'])

    @mock.patch('data_research.scripts.'
                'load_mortgage_performance_csv.load_values')
    def test_run_load_csv(self, mock_load):
        run_csv_loader()
        self.assertEqual(mock_load.call_count, 1)

    @mock.patch('data_research.scripts.'
                'load_aggregates.load_msa_values')
    def test_run_aggregates(self, mock_load):
        load_dates()
        run_aggregates()
        self.assertEqual(mock_load.call_count, len(FIPS.dates))
