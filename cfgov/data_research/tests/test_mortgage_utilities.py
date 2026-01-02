from unittest import mock

import django

from data_research.models import MortgageDataConstant
from data_research.mortgage_utilities.fips_meta import (
    County,
    State,
    load_constants,
    load_counties,
    load_states,
)


class LoadConstantsTest(django.test.TestCase):
    fixtures = ["mortgage_constants.json", "mortgage_metadata.json"]

    @mock.patch("data_research.mortgage_utilities.fips_meta.FIPS")
    def test_constants_loading(self, mock_FIPS):
        target_starting_date = MortgageDataConstant.objects.get(
            name="starting_date"
        ).date_value
        load_constants()
        self.assertEqual(mock_FIPS.starting_date, target_starting_date)


class GeoLoadTest(django.test.TestCase):
    def test_state_county_loading(self):
        """County loading depends on States, so testing together."""
        State.objects.all().delete()
        self.assertEqual(State.objects.count(), 0)
        load_states()
        self.assertEqual(State.objects.count(), 51)
        County.objects.all().delete()
        self.assertEqual(County.objects.count(), 0)
        load_counties()
        self.assertEqual(County.objects.count(), 3148)
