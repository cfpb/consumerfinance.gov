from unittest import mock

import django

from data_research.models import MortgageDataConstant
from data_research.mortgage_utilities.fips_meta import load_constants


class LoadConstantsTest(django.test.TestCase):

    fixtures = ['mortgage_constants.json', 'mortgage_metadata.json']

    @mock.patch('data_research.mortgage_utilities.fips_meta.FIPS')
    def test_constants_loading(self, mock_FIPS):
        target_starting_date = MortgageDataConstant.objects.get(
            name='starting_date').date_value
        load_constants()
        self.assertEqual(mock_FIPS.starting_date, target_starting_date)
