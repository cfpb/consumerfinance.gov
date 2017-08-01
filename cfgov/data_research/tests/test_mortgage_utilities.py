from __future__ import unicode_literals
import unittest
import datetime

import django
import mock
from mock import mock_open, patch
from model_mommy import mommy

from data_research.mortgage_utilities.fips_meta import (
    update_valid_geos,
    validate_geo,
)
from data_research.models import (
    CountyMortgageData,
    MSAMortgageData,
    NationalMortgageData,
    StateMortgageData
)


class MortgageMetaTests(django.test.TestCase):
    """
    Make sure our validator finds counties, metros and states that meet
    our threshold requirements.
    """
    #  constants are consulted to set thresholds.
    fixtures = ['mortgage_constants.json']

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
            current=25008,
            date=datetime.date(2008, 1, 1),
            fips='12',
            id=1,
            ninety=4069,
            other=3619,
            sixty=2758,
            thirty=6766,
            total=46748)

        mommy.make(
            StateMortgageData,
            current=250081,
            date=datetime.date(2008, 2, 1),
            fips='12',
            id=2,
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

        # print_patch = mock.patch(
        #     'data_research.mortgage_utilities.fips_meta.print'
        # )
        # print_patch.start()
        # self.addCleanup(print_patch.stop)

    def test_validate_county_threshold(self):
        """Validator should OK counties and metros that meet our thresholds."""
        self.assertTrue(validate_geo('county', '12081', 2008, 1000))
        self.assertTrue(validate_geo('msa', '35840', 2008, 1000))

    def test_validate_county_threshold_enforces_threshold(self):
        """Make sure our validator excludes geos under the threshold."""
        self.assertFalse(validate_geo('county', '16079', 2008, 1000))

    @mock.patch('data_research.mortgage_utilities.fips_meta.validate_geo')
    @mock.patch('data_research.mortgage_utilities.fips_meta.FIPS')
    @mock.patch('data_research.mortgage_utilities.fips_meta.load_fips_meta')
    def test_update_valid_geos(
            self, mock_load_fips_meta, mock_FIPS, mock_validate_geo):
        mock_FIPS.county_fips = {'12081': ''}
        mock_FIPS.msa_fips = {'35840': ''}
        mock_FIPS.state_fips = {'12': ''}
        mock_FIPS.threshold_year = 2016
        mock_FIPS.threshold_count = 1000
        m = mock_open()
        with patch('__builtin__.open', m, create=True):
            update_valid_geos()
        self.assertEqual(m.call_count, 1)
        self.assertEqual(mock_load_fips_meta.call_count, 1)
        self.assertEqual(mock_validate_geo.call_count, 3)
