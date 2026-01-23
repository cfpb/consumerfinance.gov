from unittest import mock

import django

from data_research.models import MortgageDataConstant, MortgageMetaData
from data_research.mortgage_utilities.fips_meta import (
    FIPS,
    County,
    MetroArea,
    State,
    assemble_msa_mapping,
    load_constants,
    load_counties,
    load_county_mappings,
    load_metros,
    load_states,
    update_geo_meta,
)


class GeoMetaUpdateTest(django.test.TestCase):
    fixtures = ["mortgage_county_metro.json"]
    expected_county_fips = [
        "33001",
        "33003",
        "33005",
        "33007",
        "33009",
        "33011",
        "33013",
        "33015",
        "33017",
        "33019",
    ]
    expected_msa_fips = ["14460", "31700"]
    meta_model = MortgageMetaData

    def test_load_county_mappings(self):
        FIPS.state_fips = MortgageMetaData.objects.get(
            name="state_meta"
        ).json_value
        FIPS.msa_fips = assemble_msa_mapping()
        load_county_mappings()
        self.assertIn("33", FIPS.state_fips)
        self.assertEqual(FIPS.state_fips["33"]["abbr"], "NH")
        self.assertEqual(len(FIPS.state_fips["33"]["counties"]), 10)

    def test_update_geo_meta_invalid_name(self):
        response = update_geo_meta("metros")
        self.assertIs(response, None)

    def test_update_metro_fips(self):
        obj = self.meta_model.objects.get(name="msa_fips")
        obj.json_value = []
        obj.save()
        test_resp = update_geo_meta("metro")
        self.assertEqual(test_resp, "metro meta updated")
        new_vals = self.meta_model.objects.get(name="msa_fips").json_value
        self.assertEqual(new_vals, self.expected_msa_fips)

    def test_update_county_fips(self):
        obj = self.meta_model.objects.get(name="county_fips")
        obj.json_value = []
        obj.save()
        test_resp = update_geo_meta("county")
        self.assertEqual(test_resp, "county meta updated")
        new_vals = self.meta_model.objects.get(name="county_fips").json_value
        self.assertEqual(new_vals, self.expected_county_fips)


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

    def test_metro_loading(self):
        MetroArea.objects.all().delete()
        self.assertEqual(MetroArea.objects.count(), 0)
        load_metros()
        self.assertEqual(MetroArea.objects.count(), 925)
