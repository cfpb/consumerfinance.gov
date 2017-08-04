from __future__ import unicode_literals

import datetime
import mock
import unittest

import django.test
from model_mommy import mommy

from data_research.models import StateMortgageData, MSAMortgageData
from data_research.scripts.load_mortgage_performance_csv import (
    CountyMortgageData,
    validate_fips,
    load_values,
)
from data_research.scripts.load_mortgage_aggregates import (
    load_msa_values,
    load_national_values,
    load_state_values,
    run as run_aggregates)


class AggregateLoadTest(django.test.TestCase):
    """Tests aggregate loading function"""

    def setUp(self):

        print_patch = mock.patch(
            'data_research.scripts.load_mortgage_aggregates.print'
        )
        print_patch.start()
        self.addCleanup(print_patch.stop)

    @mock.patch('data_research.scripts.'
                'load_mortgage_aggregates.load_fips_meta')
    def test_load_msa_values(self, mock_load_meta):
        from data_research.scripts.load_mortgage_aggregates import (
            FIPS, MSAMortgageData, load_msa_values)
        FIPS.msa_fips = {
            '45300':
            {'msa': 'Tampa-St. Petersburg-Clearwater, FL',
             'county_list': ['12081']}}
        date = "2016-09-01"
        load_msa_values(date)
        self.assertEqual(MSAMortgageData.objects.count(), 1)


class DataLoadTest(django.test.TestCase):
    """Tests loading functions"""

    fixtures = ['mortgage_constants.json']

    def setUp(self):

        mommy.make(
            MSAMortgageData,
            current=5250,
            date=datetime.date(2008, 1, 1),
            fips='35840',
            id=1,
            ninety=1406,
            other=361,
            sixty=1275,
            thirty=3676,
            total=22674)

        mommy.make(
            StateMortgageData,
            current=250081,
            date=datetime.date(2008, 1, 1),
            fips='12',
            id=1,
            ninety=4069,
            other=3619,
            sixty=2758,
            thirty=6766,
            total=26748)

        print_patch = mock.patch(
            'data_research.scripts.load_mortgage_performance_csv.print'
        )
        print_patch.start()
        self.addCleanup(print_patch.stop)

        print_patch2 = mock.patch(
            'data_research.scripts.load_mortgage_aggregates.print'
        )
        print_patch2.start()
        self.addCleanup(print_patch2.stop)

    @mock.patch('data_research.scripts.load_mortgage_aggregates.'
                'MSAMortgageData.objects.get_or_create')
    @mock.patch('data_research.scripts.load_mortgage_aggregates.FIPS')
    def test_load_msa_values(self, mock_FIPS, mock_get_or_create):
        mock_FIPS.msa_fips = {'35840': {'county_list': ['12081']}}
        msa = MSAMortgageData.objects.first()
        mock_get_or_create.return_value = msa, False
        load_msa_values('2008-01-01')
        self.assertEqual(mock_get_or_create.call_count, 1)

    @mock.patch('data_research.scripts.load_mortgage_aggregates.'
                'StateMortgageData.objects.get_or_create')
    @mock.patch('data_research.scripts.load_mortgage_aggregates.FIPS')
    def test_load_state_values(self, mock_FIPS, mock_get_or_create):
        mock_FIPS.state_fips = {'12': ''}
        state = StateMortgageData.objects.first()
        mock_get_or_create.return_value = state, True
        load_state_values('2008-01-01')
        self.assertEqual(mock_get_or_create.call_count, 1)
        mock_get_or_create.return_value = state, False
        load_state_values('2008-01-01')
        self.assertEqual(mock_get_or_create.call_count, 2)

    def test_load_national_values(self):
        from data_research.models import NationalMortgageData
        load_national_values('2016-09-01')
        self.assertEqual(NationalMortgageData.objects.count(), 1)
        load_national_values('2016-09-01')
        self.assertEqual(NationalMortgageData.objects.count(), 1)

    @mock.patch('data_research.scripts.'
                'load_mortgage_performance_csv.read_in_s3_csv')
    def test_load_values(self, mock_read_in):
        mock_read_in.return_value = [{
            'thirty': '4', 'month': '1', 'current': '262', 'sixty': '1',
            'ninety': '0', 'date': '01/01/98', 'open': '270', 'other': '3',
            'fips': '01001'}]
        load_values()
        self.assertEqual(mock_read_in.call_count, 1)
        self.assertEqual(CountyMortgageData.objects.count(), 1)

    @mock.patch('data_research.scripts.'
                'load_mortgage_performance_csv.read_in_s3_csv')
    def test_load_values_return_fips(self, mock_read_in):
        mock_read_in.return_value = [{
            'thirty': '4', 'month': '1', 'current': '262', 'sixty': '1',
            'ninety': '0', 'date': '01/01/98', 'open': '270', 'other': '3',
            'fips': '01001'}]
        fips_list = load_values(return_fips=True)
        self.assertEqual(mock_read_in.call_count, 1)
        self.assertEqual(fips_list, ['01001'])


class DataScriptTest(unittest.TestCase):
    """Tests for data pipeline automations"""

    def setUp(self):
        print_patch = mock.patch(
            'data_research.scripts.load_mortgage_performance_csv.print'
        )
        print_patch.start()
        self.addCleanup(print_patch.stop)

        print_patch2 = mock.patch(
            'data_research.scripts.load_mortgage_aggregates.print'
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

    def test_validate_fips_outdated_fips(self):
        fips_input = '02201'  # a normally excluded outdated FIPS code
        self.assertIs(validate_fips(fips_input), None)

    def test_validate_fips_keep_outdated(self):
        fips_input = '02201'  # a normally excluded outdated FIPS code
        self.assertEqual(validate_fips(
            fips_input, keep_outdated=True), '02201')

    @mock.patch('data_research.scripts.'
                'load_mortgage_aggregates.load_fips_meta')
    @mock.patch('data_research.scripts.'
                'load_mortgage_aggregates.load_msa_values')
    @mock.patch('data_research.scripts.'
                'load_mortgage_aggregates.load_state_values')
    @mock.patch('data_research.scripts.'
                'load_mortgage_aggregates.load_national_values')
    def test_run_aggregates(self, mock_load_national, mock_load_states,
                            mock_load_msas, mock_load_fips):
        from data_research.scripts.load_mortgage_aggregates import FIPS
        FIPS.dates = ['2016-09-01']
        run_aggregates()
        self.assertEqual(mock_load_fips.call_count, 1)
        self.assertEqual(mock_load_national.call_count, 1)
        self.assertEqual(mock_load_states.call_count, 1)
        self.assertEqual(mock_load_msas.call_count, 1)

    @mock.patch('data_research.scripts.'
                'load_mortgage_performance_csv.load_values')
    def test_run_csv_load(self, mock_load):
        from data_research.scripts import load_mortgage_performance_csv
        load_mortgage_performance_csv.run()
        self.assertEqual(mock_load.call_count, 1)
