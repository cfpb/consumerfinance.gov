from __future__ import unicode_literals

import django
import mock

from data_research.mortgage_utilities.fips_meta import load_constants


class LoadConstantsTest(django.test.TestCase):

    @mock.patch('data_research.mortgage_utilities.fips_meta.FIPS')
    def test_constants_no_models(self, mock_FIPS):
        load_constants()
        self.assertEqual(mock_FIPS.starting_year, 2008)
