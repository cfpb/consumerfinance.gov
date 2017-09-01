from __future__ import unicode_literals
import datetime

import django
import mock
from mock import mock_open, patch
from model_mommy import mommy

from data_research.mortgage_utilities.fips_meta import load_constants
from data_research.scripts.validate_geos import (
    update_valid_geos,
    validate_geo,
)
from data_research.models import (
    CountyMortgageData,
    MSAMortgageData,
    NationalMortgageData,
    StateMortgageData
)


class LoadConstantsTest(django.test.TestCase):

    @mock.patch('data_research.mortgage_utilities.fips_meta.FIPS')
    def test_constants_no_models(self, mock_FIPS):
        load_constants()
        self.assertEqual(mock_FIPS.starting_year, 2008)


class MortgageMetaTests(django.test.TestCase):
    """
    Make sure our validator finds counties, metros and states that meet
    our threshold requirements.
    """
    #  constants are consulted to set thresholds.

    fixtures = ['mortgage_constants.json', 'mortgage_metadata.json']

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
            CountyMortgageData,
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

        mommy.make(
            CountyMortgageData,
            current=250,
            date=datetime.date(2008, 1, 1),
            fips='16079',
            id=2,
            ninety=10,
            other=10,
            sixty=10,
            thirty=10,
            total=290)

    def test_validate_county_threshold(self):
        """Validator should OK counties and metros that meet our thresholds."""
        self.assertTrue(validate_geo('county', '12081', 2008, 1000))
        self.assertTrue(validate_geo('msa', '35840', 2008, 1000))

    def test_validate_county_threshold_enforces_threshold(self):
        """Make sure our validator excludes geos under the threshold."""
        self.assertFalse(validate_geo('county', '16079', 2008, 1000))

    @mock.patch('data_research.scripts.validate_geos.validate_geo')
    @mock.patch('data_research.scripts.validate_geos.FIPS')
    @mock.patch('data_research.scripts.validate_geos.load_fips_meta')
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
        # validate_geo should be called for county, metro, non-metro and state
        self.assertEqual(mock_validate_geo.call_count, 4)
        self.assertIs(
            CountyMortgageData.objects.get(fips='12081').valid,
            True)
        self.assertIs(
            StateMortgageData.objects.get(fips='12').valid,
            True)
        self.assertIs(
            MSAMortgageData.objects.get(fips='35840').valid,
            True)
