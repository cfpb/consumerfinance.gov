import datetime
import unittest

import django
from django.http import HttpRequest

from model_bakery import baker

from data_research.models import (
    County,
    CountyMortgageData,
    MetroArea,
    MortgageDataConstant,
    MortgageMetaData,
    MortgagePerformancePage,
    MSAMortgageData,
    NationalMortgageData,
    NonMSAMortgageData,
    State,
    StateMortgageData,
)
from data_research.mortgage_utilities.fips_meta import FIPS, load_fips_meta


class GeoValidationTests(django.test.TestCase):
    """
    Check the functions that validate metro, non-metro and county areas
    against our data thresholds.
    """

    fixtures = ["mortgage_metadata.json", "mortgage_constants.json"]

    def setUp(self):

        baker.make(
            State,
            fips="12",
            name="Florida",
            abbr="FL",
            ap_abbr="Fla.",
            counties=["12013", "12081"],
            non_msa_counties=["12013"],
            msas=["45300", "35840", "45220"],
        )

        baker.make(
            State,
            fips="34",
            name="New Jersey",
            abbr="NJ",
            ap_abbr="N.J.",
            counties=[],
            non_msa_counties=[],
            msas=[],
        )

        baker.make(
            MetroArea,
            fips="45220",
            name="Tallahassee, FL",
            counties=["12039"],
            states=["12"],
            valid=False,
        )

        baker.make(
            MetroArea,
            fips="35840",
            name="North Port-Sarasota-Bradenton, FL",
            counties=["12081"],
            states=["12"],
            valid=True,
        )

        baker.make(
            County,
            fips="12081",
            name="Manatee County",
            state=State.objects.get(fips="12"),
            valid=False,
        )

        baker.make(
            County,
            fips="12039",
            name="Gadsden County",
            state=State.objects.get(fips="12"),
            valid=False,
        )

        baker.make(
            County,
            fips="12013",
            name="Calhoun County",
            state=State.objects.get(fips="12"),
            valid=True,
        )

        baker.make(
            MSAMortgageData,
            date=datetime.date(2016, 1, 1),
            fips="45220",
            total="200",
            current="100",
            thirty="50",
            sixty="0",
            ninety="50",
            other="0",
            msa=MetroArea.objects.get(fips="45220"),
        )

        baker.make(
            MSAMortgageData,
            date=datetime.date(2016, 1, 1),
            fips="35840",
            total="2000",
            current="500",
            thirty="500",
            sixty="500",
            ninety="500",
            other="0",
            msa=MetroArea.objects.get(fips="35840"),
        )

        baker.make(
            CountyMortgageData,
            date=datetime.date(2016, 1, 1),
            fips="12039",
            total="200",
            current="100",
            thirty="50",
            sixty="0",
            ninety="50",
            other="0",
            county=County.objects.get(fips="12039"),
        )

        baker.make(
            CountyMortgageData,
            date=datetime.date(2016, 1, 1),
            fips="12081",
            total="2643",
            current="2526",
            thirty="35",
            sixty="11",
            ninety="44",
            other="26",
            county=County.objects.get(fips="12081"),
        )

        baker.make(
            CountyMortgageData,
            date=datetime.date(2016, 1, 1),
            fips="12013",
            total="2643",
            current="2526",
            thirty="35",
            sixty="11",
            ninety="44",
            other="26",
            county=County.objects.get(fips="12013"),
        )

        baker.make(
            NonMSAMortgageData,
            date=datetime.date(2016, 1, 1),
            fips="12-non",
            total="200",
            current="110",
            thirty="35",
            sixty="11",
            ninety="44",
            other="0",
            state=State.objects.get(fips="12"),
        )

        baker.make(
            NonMSAMortgageData,
            date=datetime.date(2016, 1, 1),
            fips="34-non",
            total=None,
            current=None,
            thirty=None,
            sixty=None,
            ninety=None,
            other=None,
            state=State.objects.get(fips="34"),
        )

        baker.make(
            StateMortgageData,
            date=datetime.date(2016, 1, 1),
            fips="12",
            total="1000000",
            current="0",
            thirty="0",
            sixty="0",
            ninety="0",
            other="0",
        )

        baker.make(
            NationalMortgageData,
            date=datetime.date(2016, 1, 1),
            fips="-----",
            total="0",
            current="110",
            thirty="35",
            sixty="11",
            ninety="44",
            other="0",
        )

    def test_county_validation(self):
        county = County.objects.get(fips="12081")
        county_data = CountyMortgageData.objects.get(fips="12081")
        county.validate()
        self.assertIs(county.valid, True)
        county_data.total = 100
        county_data.save()
        county.validate()
        self.assertIs(county.valid, False)

    def test_msa_validation(self):
        msa = MetroArea.objects.get(fips="45220")
        msa.validate()
        self.assertIs(msa.valid, False)
        msa2 = MetroArea.objects.get(fips="35840")
        msa2.validate()
        self.assertIs(msa2.valid, True)

    def test_non_msa_validation(self):
        """Non-MSA validation occurs on the State model."""
        state = State.objects.get(fips="12")
        non_msa = NonMSAMortgageData.objects.get(fips="12-non")
        state.validate_non_msas()
        self.assertIs(state.non_msa_valid, False)
        non_msa.aggregate_data()
        state.validate_non_msas()
        self.assertIs(state.non_msa_valid, True)

    def test_non_msa_validation_no_counties(self):
        """Non-MSA validation occurs on the State model."""
        state = State.objects.get(fips="34")
        state.validate_non_msas()
        self.assertIs(state.non_msa_valid, False)

    def test_non_msa_aggregation_no_counties(self):
        non_msa_no_counties = NonMSAMortgageData.objects.get(fips="34-non")
        non_msa_no_counties.aggregate_data()
        self.assertEqual(non_msa_no_counties.total, 0)

    def test_national_aggregation(self):
        """National records aggregate state records."""
        nation_record = NationalMortgageData.objects.get(
            date=datetime.date(2016, 1, 1)
        )
        self.assertEqual(nation_record.total, 0)
        nation_record.aggregate_data()
        self.assertEqual(nation_record.total, 1000000)

    def test_state_name_string(self):
        state = State.objects.get(fips="12")
        self.assertEqual(
            state.__str__(), "{} ({})".format(state.name, state.fips)
        )

    def test_metro_name_string(self):
        metro = MetroArea.objects.get(fips="35840")
        self.assertEqual(
            metro.__str__(), "{} ({})".format(metro.name, metro.fips)
        )

    def test_county_name_string(self):
        county = County.objects.get(fips="12081")
        self.assertEqual(
            county.__str__(),
            "{}, {} ({})".format(county.name, county.state.abbr, county.fips),
        )


class MortgageBaseCountiesTest(unittest.TestCase):
    def test_bare_mortgage_base_counties(self):
        """No county_list should be applied to county data records."""
        base = CountyMortgageData()
        self.assertEqual(base.county_list, [])


class MortgagePerformancePageTests(django.test.TestCase):

    fixtures = ["mortgage_metadata.json"]

    def setUp(self):
        from v1.tests.wagtail_pages.helpers import save_new_page

        page_stub_30 = MortgagePerformancePage(
            slug="mortgages-30-89-days-delinquent", title="Mortgage Charts"
        )
        self.chart_page_30 = save_new_page(page_stub_30).as_page_object()
        page_stub_90 = MortgagePerformancePage(
            slug="mortgages-90-days-delinquent", title="Mortgage Maps"
        )
        self.map_page_90 = save_new_page(page_stub_90).as_page_object()

    def test_chart_page_get_mortgage_meta(self):
        page = self.chart_page_30
        self.assertIn("sampling_dates", page.get_mortgage_meta())

    def test_page_template(self):
        self.assertEqual(
            self.chart_page_30.template, "browse-basic/index.html"
        )

    def test_chart_page_context_30_89(self):
        test_page = self.chart_page_30
        request = HttpRequest()
        self.assertIn("delinquency", test_page.get_context(request))
        self.assertEqual(
            test_page.get_context(request)["delinquency"], "percent_30_60"
        )

    def test_chart_page_context_90(self):
        test_page = self.map_page_90
        request = HttpRequest()
        self.assertIn("delinquency", test_page.get_context(request))
        self.assertEqual(
            test_page.get_context(request)["delinquency"], "percent_90"
        )


class ModelStringTest(django.test.TestCase):

    fixtures = ["mortgage_constants.json", "mortgage_metadata.json"]

    def test_county_string_max_length(self):
        """
        Test that no MSA county-list string (a string of FIPS codes)
        will exceed the 255-char limit for `MSAMortgageData.county`
        """
        load_fips_meta()
        county_string_lengths = sorted(
            set(
                [
                    len(lister)
                    for lister in [
                        ", ".join(FIPS.msa_fips[each]["county_list"])
                        for each in FIPS.msa_fips.keys()
                    ]
                ]
            )
        )
        self.assertTrue(county_string_lengths[-1] <= 255)


class MortgageModelTests(django.test.TestCase):

    fixtures = ["mortgage_constants.json", "mortgage_metadata.json"]

    def setUp(self):

        self.base_data = baker.make(
            CountyMortgageData,
            fips="12081",
            date=datetime.date(2016, 9, 1),
            total=1270,
            current=262,
            thirty=40,
            sixty=20,
            ninety=0,
            other=3,
        )

        self.msa_data = baker.make(
            MSAMortgageData,
            total=0,
            fips="45300",
            date=datetime.date(2016, 9, 1),
        )

        self.state_obj = baker.make(
            StateMortgageData,
            total=0,
            fips="12",
            date=datetime.date(2016, 9, 1),
        )

        self.nation_obj = baker.make(
            NationalMortgageData,
            current=2500819,
            date=datetime.date(2016, 9, 1),
            fips=00000,
            id=1,
            ninety=40692,
            other=36196,
            sixty=27586,
            thirty=67668,
            total=2674899,
        )

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
            sorted(data_record.time_series("90").keys()), ["date", "value"]
        )
        self.assertEqual(
            sorted(data_record.time_series("90").values()),
            [0.0, 1472702400000],
        )

    def test_msa_data_properties(self):
        msa_record = self.msa_data
        county_record = self.base_data
        msa_record.save()
        self.assertEqual(msa_record.percent_90, county_record.percent_90)
        self.assertEqual(msa_record.percent_30_60, 0)
