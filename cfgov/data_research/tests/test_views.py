from __future__ import unicode_literals

import datetime
import json
import unittest

import django
from django.core.urlresolvers import reverse
from model_mommy import mommy

from data_research.views import validate_year_month
from data_research.models import (
    CountyMortgageData,
    MSAMortgageData,
    NationalMortgageData,
    StateMortgageData)


class YearMonthValidatorTests(unittest.TestCase):
    """check the year_month validator"""
    good_pair = '2016-09'
    future_year = '2040-08'
    too_old_year = '1957-08'
    bad_month = '2015-13'
    non_integer = '201A-12'
    bad_format = '201609'

    def test_validate_year_month_good(self):
        self.assertTrue(validate_year_month(self.good_pair))

    def test_validate_year_month_future_year(self):
        self.assertFalse(validate_year_month(self.future_year))

    def test_validate_year_month_too_old(self):
        self.assertFalse(validate_year_month(self.too_old_year))

    def test_validate_year_month_bad_month(self):
        self.assertFalse(validate_year_month(self.bad_month))

    def test_validate_year_month_non_integer(self):
        self.assertFalse(validate_year_month(self.non_integer))

    def test_validate_year_month_bad_format(self):
        self.assertFalse(validate_year_month(self.bad_format))


class TimeseriesViewTests(django.test.TestCase):

    def setUp(self):
        mommy.make(
            NationalMortgageData,
            current=2500819,
            date=datetime.date(2008, 1, 1),
            fips=00000,
            id=1,
            ninety=40692,
            other=36196,
            sixty=27586,
            thirty=67668,
            total=2674899)

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
            CountyMortgageData,
            current=250,
            date=datetime.date(2008, 1, 1),
            fips='12081',
            id=1,
            ninety=406,
            other=361,
            sixty=275,
            thirty=676,
            total=2674)

    def test_national_timesereis(self):
        response = self.client.get(
            reverse('data_research_api_mortgage_timeseries_national'))
        self.assertEqual(response.status_code, 200)

    def test_state_timesereis(self):
        response = self.client.get(
            reverse(
                'data_research_api_mortgage_timeseries',
                kwargs={'fips': '12'}))
        self.assertEqual(response.status_code, 200)

    def test_msa_timesereis(self):
        response = self.client.get(
            reverse(
                'data_research_api_mortgage_timeseries',
                kwargs={'fips': '35840'}))
        self.assertEqual(response.status_code, 200)

    def test_county_timesereis(self):
        response = self.client.get(
            reverse(
                'data_research_api_mortgage_timeseries',
                kwargs={'fips': '12081'}))
        self.assertEqual(response.status_code, 200)

    def test_timesereis_bad_fips(self):
        response = self.client.get(
            reverse(
                'data_research_api_mortgage_timeseries',
                kwargs={'fips': '99999'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual('"FIPS code not found"', response.content)

    def test_map_data_bad_date(self):
        response = self.client.get(
            reverse(
                'data_research_api_mortgage_county_mapdata',
                kwargs={'geo': 'counties', 'year_month': '0000-01'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual('"Invalid year-month pair"', response.content)

    def test_county_map_data(self):
        response = self.client.get(
            reverse(
                'data_research_api_mortgage_county_mapdata',
                kwargs={'geo': 'counties', 'year_month': '2008-01'}))
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(
            sorted(response_data.get('data').get('12081').keys()),
            ['name', 'pct30', 'pct90'])

    def test_msa_map_data(self):
        response = self.client.get(
            reverse(
                'data_research_api_mortgage_metro_mapdata',
                kwargs={'geo': 'metros', 'year_month': '2008-01'}))
        self.assertEqual(response.status_code, 200)

    def test_state_map_data(self):
        response = self.client.get(
            reverse(
                'data_research_api_mortgage_state_mapdata',
                kwargs={'geo': 'states', 'year_month': '2008-01'}))
        self.assertEqual(response.status_code, 200)
