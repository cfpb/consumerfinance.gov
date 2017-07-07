from __future__ import unicode_literals
import datetime
import mock
import unittest

# import mock
# from mock import mock_open, patch
from model_mommy import mommy
# import unittest

import django.test

from data_research.models import CountyMortgageData, MSAMortgageData
from data_research.views import FIPS, load_fips_meta


class ModelStringTest(unittest.TestCase):

    def setUp(self):
        print_patch = mock.patch(
            'data_research.scripts.load_aggregates.print'
        )
        print_patch.start()
        self.addCleanup(print_patch.stop)

    def test_county_string_max_length(self):
        """
        Test that no MSA county-list string (a string of FIPS codes)
        will exceed the 255-char limit for MSAMortgageData.county.
        """
        load_fips_meta()
        county_string_lengths = sorted(set([
            len(lister) for lister in [
                ", ".join(FIPS.msa_fips[each]['county_list'])
                for each in FIPS.msa_fips.keys()
            ]
        ]))
        self.assertTrue(county_string_lengths[-1] <= 255)


class ResearchModelTests(django.test.TestCase):

    def setUp(self):

        self.base_data = mommy.make(
            CountyMortgageData,
            fips='01001',
            date=datetime.date(2016, 9, 1),
            total=270,
            current=262,
            thirty=4,
            sixty=1,
            ninety=0,
            other=3)

        self.msa_data = mommy.make(
            MSAMortgageData,
            total=0,
            fips='45300',
            date=datetime.date(2016, 9, 1),
            counties='01001')

        print_patch = mock.patch(
            'data_research.scripts.load_aggregates.print'
        )
        print_patch.start()
        self.addCleanup(print_patch.stop)

    def test_base_data_properties(self):
        """Test basic calculation functions"""
        data_record = self.base_data
        self.assertEqual(data_record.percent_30_60, 2.0)
        self.assertEqual(data_record.percent_90, 0.0)
        self.assertEqual(data_record.epoch, 1472702400)

    def test_base_data_properties_total_zero(self):
        """No divide-by-zeroes up in here."""
        data_record = self.base_data
        data_record.total = 0
        self.assertEqual(data_record.percent_90, 0)
        self.assertEqual(data_record.percent_30_60, 0)

    def test_base_data_properties_time_series(self):
        data_record = self.base_data
        self.assertEqual(
            sorted(data_record.time_series.keys()),
            ['date', 'pct30', 'pct90'])
        self.assertEqual(
            sorted(data_record.time_series.values()),
            [0.0, 2.0, 1472702400])

    def test_msa_data_properties(self):
        msa_record = self.msa_data
        county_record = self.base_data
        msa_record.save()
        self.assertEqual(
            msa_record.percent_90, county_record.percent_90)
        self.assertEqual(
            msa_record.percent_30_60, county_record.percent_30_60)
