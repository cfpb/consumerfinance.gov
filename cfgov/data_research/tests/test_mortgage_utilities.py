from __future__ import unicode_literals

import django
import mock

from data_research.mortgage_utilities.fips_meta import load_constants
from data_research.models import MortgageDataConstant


class LoadConstantsTest(django.test.TestCase):

    fixtures = ['mortgage_constants.json', 'mortgage_metadata.json']

    @mock.patch('data_research.mortgage_utilities.fips_meta.FIPS')
    def test_constants_loading(self, mock_FIPS):
        target_starting_year = MortgageDataConstant.objects.get(
            name='starting_year').value
        load_constants()
        self.assertEqual(mock_FIPS.starting_year, target_starting_year)

    @mock.patch('data_research.mortgage_utilities.fips_meta.FIPS')
    def test_missing_constant(self, mock_FIPS):
        default_starting_year = 2008
        MortgageDataConstant.objects.get(name='starting_year').delete()
        load_constants()
        self.assertEqual(mock_FIPS.starting_year, default_starting_year)
