import datetime
import json
import unittest

import django
from django.urls import NoReverseMatch, reverse

from model_bakery import baker

from data_research.models import (
    County, CountyMortgageData, MetroArea, MSAMortgageData,
    NationalMortgageData, NonMSAMortgageData, State, StateMortgageData
)
from data_research.views import validate_year_month


class YearMonthValidatorTests(unittest.TestCase):
    """check the year_month validator"""

    good_pair = "2016-09"
    future_year = "2040-08"
    too_old_year = "1957-08"
    bad_month = "2015-13"
    non_integer = "201A-12"
    bad_format = "201609"

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

    fixtures = ["mortgage_constants.json", "mortgage_metadata.json"]

    def setUp(self):
        baker.make(
            State,
            fips="12",
            abbr="FL",
            ap_abbr="Fla.",
            counties=["12081"],
            msas=["52081"],
            name="Florida",
            non_msa_counties=["12001"],
            non_msa_valid=True,
        )

        baker.make(
            County,
            fips="12081",
            name="Manatee County",
            state=State.objects.get(fips="12"),
            valid=True,
        )

        baker.make(
            MetroArea,
            fips="35840",
            name="North Port-Sarasota-Bradenton, FL",
            states=["12"],
            counties=["12081", "12115"],
            valid=True,
        )

        baker.make(
            MetroArea,
            fips="16220",
            name="Casper, WY",
            states=["56"],
            counties=["12081", "12115"],
            valid=True,
        )

        baker.make(
            NationalMortgageData,
            current=2500819,
            date=datetime.date(2008, 1, 1),
            fips="-----",
            id=1,
            ninety=40692,
            other=36196,
            sixty=27586,
            thirty=67668,
            total=2674899,
        )

        baker.make(
            StateMortgageData,
            current=250081,
            date=datetime.date(2008, 1, 1),
            fips="12",
            id=1,
            state=State.objects.get(fips="12"),
            ninety=4069,
            other=3619,
            sixty=2758,
            thirty=6766,
            total=26748,
        )

        baker.make(
            MSAMortgageData,
            current=5250,
            date=datetime.date(2008, 1, 1),
            msa=MetroArea.objects.get(fips="35840"),
            fips="35840",
            id=1,
            ninety=1406,
            other=361,
            sixty=1275,
            thirty=3676,
            total=22674,
        )

        baker.make(
            NonMSAMortgageData,
            current=5250,
            date=datetime.date(2008, 1, 1),
            state=State.objects.get(fips="12"),
            fips="12-non",
            id=1,
            ninety=1406,
            other=361,
            sixty=1275,
            thirty=3676,
            total=22674,
        )

        baker.make(
            CountyMortgageData,
            current=250,
            date=datetime.date(2008, 1, 1),
            county=County.objects.get(fips="12081"),
            fips="12081",
            id=1,
            ninety=406,
            other=361,
            sixty=275,
            thirty=676,
            total=2674,
        )

    def test_metadata_request(self):
        response = self.client.get(
            reverse(
                "data_research_api_metadata",
                kwargs={"meta_name": "sampling_dates"},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("2008-01-01", json.loads(response.content))

    def test_metadata_request_bad_meta_name(self):
        response = self.client.get(
            reverse("data_research_api_metadata", kwargs={"meta_name": "xxx"})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No metadata object found.")

    def test_national_timeseries_30_89(self):
        response = self.client.get(
            reverse(
                "data_research_api_mortgage_timeseries_national",
                kwargs={"days_late": "30-89"},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_national_timeseries_90(self):
        response = self.client.get(
            reverse(
                "data_research_api_mortgage_timeseries_national",
                kwargs={"days_late": "90"},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_state_timeseries_30_89(self):
        response = self.client.get(
            reverse(
                "data_research_api_mortgage_timeseries",
                kwargs={"fips": "12", "days_late": "30-89"},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_state_timeseries_90(self):
        response = self.client.get(
            reverse(
                "data_research_api_mortgage_timeseries",
                kwargs={"fips": "12", "days_late": "90"},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_msa_timeseries_30_89(self):
        response = self.client.get(
            reverse(
                "data_research_api_mortgage_timeseries",
                kwargs={"fips": "35840", "days_late": "30-89"},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_msa_timeseries_90(self):
        response = self.client.get(
            reverse(
                "data_research_api_mortgage_timeseries",
                kwargs={"fips": "35840", "days_late": "90"},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_msa_timeseries_90_below_threshold(self):
        response = self.client.get(
            reverse(
                "data_research_api_mortgage_timeseries",
                kwargs={"fips": "16220", "days_late": "90"},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "not valid")

    def test_non_msa_timeseries_30_89(self):
        response = self.client.get(
            reverse(
                "data_research_api_mortgage_timeseries",
                kwargs={"fips": "12-non", "days_late": "30-89"},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_non_msa_timeseries_90(self):
        response = self.client.get(
            reverse(
                "data_research_api_mortgage_timeseries",
                kwargs={"fips": "12-non", "days_late": "90"},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_county_timeseries_30_89(self):
        response = self.client.get(
            reverse(
                "data_research_api_mortgage_timeseries",
                kwargs={"fips": "12081", "days_late": "30-89"},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_county_timeseries_90(self):
        response = self.client.get(
            reverse(
                "data_research_api_mortgage_timeseries",
                kwargs={"fips": "12081", "days_late": "90"},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_timeseries_bad_fips(self):
        response = self.client.get(
            reverse(
                "data_research_api_mortgage_timeseries",
                kwargs={"fips": "99999", "days_late": "90"},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "FIPS code not found")

    def test_map_data_bad_date(self):
        response = self.client.get(
            reverse(
                "data_research_api_mortgage_mapdata",
                kwargs={
                    "geo": "counties",
                    "days_late": "90",
                    "year_month": "0000-01",
                },
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid year-month pair")

    def test_map_data_disallowed_delinquency_digit(self):
        with self.assertRaises(NoReverseMatch):
            self.client.get(
                reverse(
                    "data_research_api_mortgage_mapdata",
                    kwargs={
                        "geo": "counties",
                        "days_late": "100",
                        "year_month": "2008-01",
                    },
                )
            )

    def test_map_data_disallowed_delinquency_range(self):
        response = self.client.get(
            reverse(
                "data_research_api_mortgage_mapdata",
                kwargs={
                    "geo": "counties",
                    "days_late": "38-89",
                    "year_month": "2008-01",
                },
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Unknown delinquency range")

    def test_timeseries_disallowed_delinquency_range(self):
        response = self.client.get(
            reverse(
                "data_research_api_mortgage_timeseries",
                kwargs={"fips": "12081", "days_late": "38-89"},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Unknown delinquency range")

    def test_national_timeseries_disallowed_delinquency_range(self):
        response = self.client.get(
            reverse(
                "data_research_api_mortgage_timeseries_national",
                kwargs={"days_late": "38-89"},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Unknown delinquency range")

    def test_map_data_unknown_geo(self):
        response = self.client.get(
            reverse(
                "data_research_api_mortgage_mapdata",
                kwargs={
                    "geo": "parish",
                    "days_late": "90",
                    "year_month": "2008-01",
                },
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Unkown geographic unit")

    def test_county_map_data_30_89(self):
        response = self.client.get(
            reverse(
                "data_research_api_mortgage_mapdata",
                kwargs={
                    "geo": "counties",
                    "days_late": "30-89",
                    "year_month": "2008-01",
                },
            )
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(
            sorted(response_data.get("data").get("12081").keys()),
            ["name", "value"],
        )

    def test_county_map_data_90(self):
        response = self.client.get(
            reverse(
                "data_research_api_mortgage_mapdata",
                kwargs={
                    "geo": "counties",
                    "days_late": "90",
                    "year_month": "2008-01",
                },
            )
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(
            sorted(response_data.get("data").get("12081").keys()),
            ["name", "value"],
        )

    def test_msa_map_data_30_89(self):
        response = self.client.get(
            reverse(
                "data_research_api_mortgage_mapdata",
                kwargs={
                    "geo": "metros",
                    "days_late": "30-89",
                    "year_month": "2008-01",
                },
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_msa_map_data_90(self):
        response = self.client.get(
            reverse(
                "data_research_api_mortgage_mapdata",
                kwargs={
                    "geo": "metros",
                    "days_late": "90",
                    "year_month": "2008-01",
                },
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_map_view_msa_below_threshold(self):
        """The view should deliver a below-threshold MSA with value of None"""
        msa = MSAMortgageData.objects.get(fips="35840")
        geo = msa.msa
        geo.valid = False
        geo.save()
        response = self.client.get(
            reverse(
                "data_research_api_mortgage_mapdata",
                kwargs={
                    "geo": "metros",
                    "days_late": "90",
                    "year_month": "2008-01",
                },
            )
        )
        self.assertEqual(response.status_code, 200)
        msa_value = json.loads(response.content)["data"][msa.fips]["value"]
        self.assertIs(msa_value, None)

    def test_map_view_non_msa_below_threshold(self):
        """Should deliver a below-threshold non-MSA with value of None"""
        non_msa = NonMSAMortgageData.objects.get(fips="12-non")
        geo = non_msa.state
        geo.non_msa_valid = False
        geo.save()
        response = self.client.get(
            reverse(
                "data_research_api_mortgage_mapdata",
                kwargs={
                    "geo": "metros",
                    "days_late": "90",
                    "year_month": "2008-01",
                },
            )
        )
        self.assertEqual(response.status_code, 200)
        msa_value = json.loads(response.content)["data"][non_msa.fips]["value"]
        self.assertIs(msa_value, None)

    def test_national_map_data_30_89(self):
        response = self.client.get(
            reverse(
                "data_research_api_mortgage_mapdata",
                kwargs={
                    "geo": "national",
                    "days_late": "30-89",
                    "year_month": "2008-01",
                },
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_national_map_data_90(self):
        response = self.client.get(
            reverse(
                "data_research_api_mortgage_mapdata",
                kwargs={
                    "geo": "national",
                    "days_late": "90",
                    "year_month": "2008-01",
                },
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_county_timeseries_data_invalid(self):
        county = County.objects.get(fips="12081")
        county.valid = False
        county.save()
        response = self.client.get(
            reverse(
                "data_research_api_mortgage_timeseries",
                kwargs={"fips": "12081", "days_late": "90"},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "County is below display threshold")
