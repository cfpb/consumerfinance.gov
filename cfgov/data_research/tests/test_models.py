from __future__ import unicode_literals
import datetime
import unittest

from model_mommy import mommy

import django.test

from data_research.models import (
    CountyMortgageData,
    MortgageDataConstant,
    MortgageMetaData,
    MSAMortgageData,
    NationalMortgageData,
    StateMortgageData
)
from data_research.mortgage_utilities.fips_meta import FIPS, load_fips_meta


class ModelStringTest(unittest.TestCase):

    fixtures = ['mortgage_constants.json']

    def test_county_string_max_length(self):
        """
        Test that no MSA county-list string (a string of FIPS codes)
        will exceed the 255-char limit for `MSAMortgageData.county`
        """
        load_fips_meta()
        county_string_lengths = sorted(set([
            len(lister) for lister in [
                ", ".join(FIPS.msa_fips[each]['county_list'])
                for each in FIPS.msa_fips.keys()
            ]
        ]))
        self.assertTrue(county_string_lengths[-1] <= 255)


class MortgageModelTests(django.test.TestCase):

    fixtures = ['mortgage_constants.json', 'mortgage_metadata.json']

    def setUp(self):

        self.base_data = mommy.make(
            CountyMortgageData,
            fips='12081',
            date=datetime.date(2016, 9, 1),
            total=1270,
            current=262,
            thirty=40,
            sixty=20,
            ninety=0,
            other=3)

        self.msa_data = mommy.make(
            MSAMortgageData,
            total=0,
            fips='45300',
            date=datetime.date(2016, 9, 1),
            counties='12081')

        self.state_obj = mommy.make(
            StateMortgageData,
            total=0,
            fips='12',
            date=datetime.date(2016, 9, 1))

        self.nation_obj = mommy.make(
            NationalMortgageData,
            current=2500819,
            date=datetime.date(2016, 9, 1),
            fips=00000,
            id=1,
            ninety=40692,
            other=36196,
            sixty=27586,
            thirty=67668,
            total=2674899)

    def test_constant_string(self):
        constant = MortgageDataConstant.objects.first()
        self.assertEqual(constant.__str__(), "{}".format(constant))

    def test_meta_string(self):
        meta = MortgageMetaData.objects.first()
        self.assertEqual(meta.__str__(), "{}".format(meta))

    def test_base_data_properties(self):
        """Test basic calculation functions"""
        data_record = self.base_data
        self.assertEqual(data_record.percent_30_60, 0.047244094488188976)
        self.assertEqual(data_record.percent_90, 0.0)
        self.assertEqual(data_record.epoch, 1472702400000)

    def test_base_data_properties_total_zero(self):
        """No divide-by-zeroes up in here."""
        data_record = self.base_data
        data_record.total = 0
        self.assertEqual(data_record.percent_90, 0)
        self.assertEqual(data_record.percent_30_60, 0)

    def test_base_data_properties_time_series(self):
        data_record = self.base_data
        self.assertEqual(
            sorted(data_record.time_series('90').keys()),
            ['date', 'value'])
        self.assertEqual(
            sorted(data_record.time_series('90').values()),
            [0.0, 1472702400000])

    def test_msa_data_properties(self):
        msa_record = self.msa_data
        county_record = self.base_data
        msa_record.save()
        self.assertEqual(
            msa_record.percent_90, county_record.percent_90)
        self.assertEqual(
            msa_record.percent_30_60, 0.047244094488188976)
