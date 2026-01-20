import datetime
import tempfile
import unittest
from datetime import date
from io import StringIO
from unittest import mock

import django

import responses
from model_bakery import baker

from data_research.models import (
    County,
    CountyMortgageData,
    MetroArea,
    MortgageMetaData,
    MSAMortgageData,
    NationalMortgageData,
    NonMSAMortgageData,
    State,
    StateMortgageData,
    validate_counties,
)
from data_research.mortgage_utilities.fips_meta import FIPS, validate_fips
from data_research.scripts.export_public_csvs import (
    bake_local,
    export_downloadable_csv,
    round_pct,
    row_starter,
    save_metadata,
)
from data_research.scripts.export_public_csvs import run as run_export
from data_research.scripts.load_mortgage_aggregates import (
    load_msa_values,
    load_national_values,
    load_non_msa_state_values,
    load_state_values,
    merge_the_dades,
    update_sampling_dates,
)
from data_research.scripts.load_mortgage_aggregates import (
    run as run_aggregates,
)
from data_research.scripts.process_mortgage_data import (
    get_thrudate,
    process_source,
    read_source_csv,
)
from data_research.scripts.process_mortgage_data import (
    run as run_process_mortgage_data,
)
from data_research.scripts.update_county_msa_meta import run as run_update
from data_research.scripts.update_county_msa_meta import (
    update_state_to_geo_meta,
)


DRS = "data_research.scripts"
DRM = "data_research.mortgage_utilities"


class ThruDateTests(unittest.TestCase):
    def test_thrudate_generation_03(self):
        latest_file = "delinquency_county_0325.csv"
        new_thrudate = get_thrudate(latest_file)
        self.assertEqual(new_thrudate, date(2024, 12, 1))

    def test_thrudate_generation_06(self):
        latest_file = "delinquency_county_0625.csv"
        new_thrudate = get_thrudate(latest_file)
        self.assertEqual(new_thrudate, date(2025, 3, 1))

    def test_thrudate_generation_09(self):
        latest_file = "delinquency_county_0925.csv"
        new_thrudate = get_thrudate(latest_file)
        self.assertEqual(new_thrudate, date(2025, 6, 1))

    def test_thrudate_generation_12(self):
        latest_file = "delinquency_county_1225.csv"
        new_thrudate = get_thrudate(latest_file)
        self.assertEqual(new_thrudate, date(2025, 9, 1))

    def test_thrudate_generation_invalid_thru_month(self):
        latest_file = "delinquency_county_0725.csv"
        with self.assertRaises(ValueError):
            get_thrudate(latest_file)

    def test_thrudate_generation_invalid_filename(self):
        with self.assertRaises(ValueError):
            get_thrudate("bad_filename.txt")


class CsvProcessingTest(unittest.TestCase):
    csvlines = [
        "RegionType,Name,CBSACode,2008-01,2008-02",
        "National,United States,-----,1.5,1.6",
        "MetroArea,Akron,10420,1.8,1.9",
    ]

    def test_bake_local(self):
        """Confirm that bake_local writes a StringIO obj to a local file."""
        with tempfile.NamedTemporaryFile(suffix=".csv") as tf:
            csvfile = StringIO()
            for line in self.csvlines:
                csvfile.write(line)
            # bake_local appends .csv to the destination file.
            bake_local("", tf.name[:-4], csvfile)
            with open(tf.name) as f:
                local_content = f.read()
            self.assertEqual(local_content, csvfile.getvalue())

    @responses.activate
    def test_read_source_csv(self):
        source_url = "https://github.local/path/to/delinquency_county_0999.csv"
        responses.add(responses.GET, source_url, body="a,b,c\nd,e,f")
        reader = read_source_csv(source_url)
        self.assertEqual(reader.fieldnames, ["a", "b", "c"])
        self.assertEqual(sorted(next(reader).values()), ["d", "e", "f"])

    @mock.patch(f"{DRS}.process_mortgage_data.process_source")
    def test_run_command_no_args(self, mock_process):
        with self.assertRaises(SystemExit):
            run_process_mortgage_data()

        self.assertEqual(mock_process.call_count, 0)


class SourceToTableTest(django.test.TestCase):
    fixtures = [
        "mortgage_states.json",
        "mortgage_counties.json",
        "mortgage_constants.json",
    ]

    start_date = datetime.date(2008, 1, 1)
    source_url = "https://github.local/path/to/delinquency_county_0925.csv"
    data_row = [
        "1",
        "01001",
        "2008-01-01",
        "1464",
        "1443",
        "10",
        "5",
        "4",
        "2",
        "2891",
    ]

    def setUp(self):
        AL = baker.make(
            State,
            fips="01",
            abbr="AL",
            name="Alabama",
            counties=[],
            non_msa_counties=[],
            msas=[],
        )

        Autauga = baker.make(
            County,
            id=2891,
            fips="01001",
            name="Autauga County",
            state=AL,
            valid=True,
        )

        baker.make(
            CountyMortgageData,
            fips="01001",
            date=self.start_date,
            total=1464,
            current=1443,
            thirty=10,
            sixty=5,
            ninety=4,
            other=2,
            county=Autauga,
        )

    @mock.patch(f"{DRS}.process_mortgage_data.read_source_csv")
    @mock.patch(f"{DRS}.process_mortgage_data.load_counties")
    @mock.patch(f"{DRS}.process_mortgage_data.load_states")
    @mock.patch(f"{DRS}.process_mortgage_data.load_metros")
    @mock.patch(f"{DRS}.process_mortgage_data.update_geo_meta")
    def test_process_source(
        self, mock_geo_meta, mock_metros, mock_states, mock_counties, mock_read
    ):
        test_data_dict = [
            {
                "date": "01/01/10",
                "fips": "12081",
                "open": "268",
                "current": "260",
                "thirty": "4",
                "sixty": "1",
                "ninety": "0",
                "other": "3",
            },
            {
                "date": "01/02/10",
                "fips": "12081",
                "open": "280",
                "current": "290",
                "thirty": "20",
                "sixty": "10",
                "ninety": "4",
                "other": "3",
            },
        ]
        mock_reader = (row for row in test_data_dict)
        mock_read.return_value = mock_reader
        process_source(self.source_url)
        self.assertEqual(CountyMortgageData.objects.count(), 2)
        self.assertEqual(mock_read.call_count, 1)
        self.assertEqual(mock_counties.call_count, 1)
        self.assertEqual(mock_states.call_count, 1)
        self.assertEqual(mock_metros.call_count, 1)
        self.assertEqual(mock_geo_meta.call_count, 2)

    @mock.patch(f"{DRS}.process_mortgage_data.process_source")
    @mock.patch(f"{DRS}.process_mortgage_data.load_mortgage_aggregates.run")
    @mock.patch(f"{DRS}.process_mortgage_data.update_county_msa_meta.run")
    @mock.patch(f"{DRS}.process_mortgage_data.export_public_csvs.run")
    def test_run_command(
        self,
        mock_export,
        mock_meta_update,
        mock_aggregates,
        mock_process_source,
    ):
        run_process_mortgage_data(self.source_url)
        self.assertEqual(mock_process_source.call_count, 1)
        self.assertEqual(mock_aggregates.call_count, 1)
        self.assertEqual(mock_meta_update.call_count, 1)
        self.assertEqual(mock_export.call_count, 1)


class DataLoadIntegrityTest(django.test.TestCase):
    fixtures = ["mortgage_constants.json", "mortgage_metadata.json"]

    def setUp(self):
        FL = baker.make(
            State,
            fips="12",
            abbr="FL",
            counties='["12081"]',
            msas='["52081"]',
            name="Florida",
            non_msa_counties='["12001"]',
            non_msa_valid=True,
        )
        FL.save()

        baker.make(
            County, fips="12081", name="Manatee County", state=FL, valid=True
        )

        # real values from a base CSV row
        self.data_header = "date,fips,open,current,thirty,sixty,ninety,other\n"
        self.data_row = "09/01/16,12081,1952,1905,21,5,10,11\n"
        self.data_row_dict = {
            "date": "09/01/16",
            "fips": "12081",
            "open": "1952",
            "current": "1905",
            "thirty": "21",
            "sixty": "5",
            "ninety": "10",
            "other": "11",
        }

    def test_validate_counties(self):
        county = County.objects.first()
        self.assertIs(county.valid, True)
        validate_counties()
        county.refresh_from_db()
        self.assertIs(county.valid, False)


class MergeTheDadesTest(django.test.TestCase):
    fixtures = ["mortgage_constants.json", "mortgage_metadata.json"]

    def setUp(self):
        self.old_dade_fips = "12025"
        self.new_dade_fips = "12086"

        baker.make(
            CountyMortgageData,
            current=100,
            date=datetime.date(2008, 1, 1),
            fips=self.old_dade_fips,
            ninety=100,
            other=100,
            sixty=100,
            thirty=100,
            total=500,
        )

        baker.make(
            CountyMortgageData,
            current=100,
            date=datetime.date(2008, 1, 1),
            fips=self.new_dade_fips,
            ninety=100,
            other=100,
            sixty=100,
            thirty=100,
            total=500,
        )

    def test_merge_the_dades(self):
        merge_the_dades()
        new_dade = CountyMortgageData.objects.get(fips=self.new_dade_fips)
        for field in ["current", "thirty", "sixty", "ninety", "other"]:
            self.assertEqual(getattr(new_dade, field), 200)
        self.assertEqual(new_dade.total, 1000)
        with self.assertRaises(CountyMortgageData.DoesNotExist):
            CountyMortgageData.objects.get(fips=self.old_dade_fips)
        # make sure a second run is idempotent
        merge_the_dades()
        for field in ["current", "thirty", "sixty", "ninety", "other"]:
            self.assertEqual(getattr(new_dade, field), 200)
        self.assertEqual(new_dade.total, 1000)

    def test_merge_the_dades_no_new_dade_record(self):
        CountyMortgageData.objects.get(fips=self.new_dade_fips).delete()
        with self.assertRaises(CountyMortgageData.DoesNotExist):
            CountyMortgageData.objects.get(fips=self.new_dade_fips)
        merge_the_dades()
        with self.assertRaises(CountyMortgageData.DoesNotExist):
            CountyMortgageData.objects.get(fips=self.old_dade_fips)


class DataExportTest(django.test.TestCase):
    """Tests exporting functions"""

    fixtures = ["mortgage_constants.json", "mortgage_metadata.json"]

    def setUp(self):
        baker.make(
            State,
            fips="12",
            abbr="FL",
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
            CountyMortgageData,
            current=1250,
            date=datetime.date(2008, 1, 1),
            county=County.objects.get(fips="12081"),
            fips="12081",
            ninety=100,
            other=100,
            sixty=100,
            thirty=100,
            total=1650,
        )

        baker.make(
            MSAMortgageData,
            current=5250,
            date=datetime.date(2008, 1, 1),
            msa=MetroArea.objects.get(fips="35840"),
            fips="35840",
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
            ninety=1406,
            other=361,
            sixty=1275,
            thirty=3676,
            total=22674,
        )

        baker.make(
            StateMortgageData,
            current=250081,
            date=datetime.date(2008, 1, 1),
            state=State.objects.get(fips="12"),
            fips="12",
            ninety=4069,
            other=3619,
            sixty=2758,
            thirty=6766,
            total=26748,
        )

        baker.make(
            NationalMortgageData,
            current=2500000,
            date=datetime.date(2008, 1, 1),
            fips="12",
            ninety=10000,
            other=10000,
            sixty=10000,
            thirty=10000,
            total=2540000,
        )

    def test_export_downloadable_csv_no_credentials(self):
        with mock.patch.object(FIPS, "dates"):
            FIPS.dates.extend(["2025-12-01"])
            FIPS.nation_row["percent_90"] = [5]
            result = export_downloadable_csv("County", "percent_90")
            self.assertIn("s3 failed", result)

    @mock.patch(f"{DRS}.export_public_csvs.bake_csv_to_s3")
    @mock.patch(f"{DRM}.fips_meta.load_fips_meta")
    @mock.patch(f"{DRM}.fips_meta.load_county_mappings")
    @mock.patch.object(FIPS, "dates")
    def test_export_downloadable_csv(
        self, mock_dates, mock_load_county, mock_load_fips, mock_bake_s3
    ):
        """The absence of LOCAL_FILEPATH should enable s3 exports."""
        run_export()
        self.assertEqual(mock_bake_s3.call_count, 6)

    @mock.patch(f"{DRS}.export_public_csvs.LOCAL_FILEPATH")
    @mock.patch(f"{DRS}.export_public_csvs.bake_local")
    @mock.patch(f"{DRM}.fips_meta.load_fips_meta")
    @mock.patch(f"{DRM}.fips_meta.load_county_mappings")
    @mock.patch.object(FIPS, "dates")
    def test_export_downloadable_csv_local(
        self,
        mock_dates,
        mock_load_county,
        mock_load_fips,
        mock_bake_local,
        mock_path="/xxx/fakepath",
    ):
        """A LOCAL_FILEPATH value should trigger local exports."""
        mock_dates.return_value = ["2026-02-012026-03-01"]
        run_export()
        self.assertEqual(mock_bake_local.call_count, 6)

    def test_row_starter(self):
        """
        def row_starter(geo_type, obj):
        if geo_type == 'County':
            return [geo_type,
                    obj.county.state.abbr,
                    obj.county.name,
                    "'{}'".format(obj.fips)]
        elif geo_type == 'MetroArea':
            return [geo_type, obj.msa.name, obj.fips]
        elif geo_type == 'State':
            return [geo_type,
                    obj.state.name,
                    "'{}'".format(obj.fips)]
        else:
            return [geo_type, obj.state.name, obj.fips]
        """
        county_data = CountyMortgageData.objects.filter(fips="12081").first()
        county = county_data.county
        county_starter = row_starter("County", county_data)
        self.assertEqual(
            county_starter,
            [
                "County",
                county.state.abbr,
                county.name,
                f"'{county_data.fips}'",
            ],
        )
        metro_data = MSAMortgageData.objects.filter(fips="35840").first()
        msa = metro_data.msa
        metro_starter = row_starter("MetroArea", metro_data)
        self.assertEqual(
            metro_starter, ["MetroArea", msa.name, metro_data.fips]
        )
        state_data = StateMortgageData.objects.filter(fips="12").first()
        state = state_data.state
        state_starter = row_starter("State", state_data)
        self.assertEqual(
            state_starter,
            ["State", state.name, f"'{state_data.fips}'"],
        )
        non_metro_data = NonMSAMortgageData.objects.get(fips="12-non")
        non_metro_starter = row_starter("NonMetroArea", non_metro_data)
        self.assertEqual(
            non_metro_starter,
            ["NonMetroArea", non_metro_data.state.name, non_metro_data.fips],
        )


class DataLoadTest(django.test.TestCase):
    """Test loading functions."""

    fixtures = ["mortgage_constants.json", "mortgage_metadata.json"]

    def setUp(self):
        FL = baker.make(
            State,
            fips="12",
            abbr="FL",
            counties='["12081"]',
            msas='["52081"]',
            name="Florida",
            non_msa_counties='["12001"]',
            non_msa_valid=True,
        )
        FL.save()

        manatee = baker.make(
            County, fips="12081", name="Manatee County", state=FL, valid=True
        )
        manatee.save()

        baker.make(
            MetroArea,
            fips="35840",
            name="North Port-Sarasota-Bradenton, FL",
            counties='["12081"]',
            states='["12"]',
            valid=True,
        )

        baker.make(
            CountyMortgageData,
            date=datetime.date(2016, 1, 1),
            fips="12081",
            county=manatee,
        )

        baker.make(
            MSAMortgageData,
            current=5250,
            date=datetime.date(2016, 1, 1),
            fips="35840",
            msa=MetroArea.objects.get(fips="35840"),
            ninety=1406,
            other=361,
            sixty=1275,
            thirty=3676,
            total=22674,
        )

        baker.make(
            NonMSAMortgageData,
            current=250081,
            date=datetime.date(2016, 1, 1),
            fips="12-non",
            state=State.objects.get(fips="12"),
            ninety=4069,
            other=3619,
            sixty=2758,
            thirty=6766,
            total=26748,
        )

        baker.make(
            StateMortgageData,
            current=250081,
            date=datetime.date(2016, 1, 1),
            state=State.objects.get(fips="12"),
            fips="12",
            ninety=4069,
            other=3619,
            sixty=2758,
            thirty=6766,
            total=26748,
        )

    def test_load_msa_values(self):
        self.assertEqual(MSAMortgageData.objects.count(), 1)
        load_msa_values("2009-12-01")
        self.assertEqual(MSAMortgageData.objects.count(), 2)

    def test_load_non_msa_state_values(self):
        self.assertEqual(State.objects.count(), 1)
        self.assertEqual(NonMSAMortgageData.objects.count(), 1)
        load_non_msa_state_values("2009-01-01")
        self.assertEqual(NonMSAMortgageData.objects.count(), 2)

    def test_load_state_values(self):
        load_state_values("2008-01-01")
        self.assertEqual(StateMortgageData.objects.count(), 2)

    def test_load_national_values(self):
        load_national_values("2016-09-01")
        self.assertEqual(NationalMortgageData.objects.count(), 1)
        load_national_values("2016-09-01")
        self.assertEqual(NationalMortgageData.objects.count(), 1)

    @mock.patch(f"{DRS}.load_mortgage_aggregates.update_sampling_dates")
    @mock.patch(f"{DRS}.load_mortgage_aggregates.validate_counties")
    def test_run_aggregates(self, mock_validate_counties, mock_update_dates):
        dates = MortgageMetaData.objects.get(name="sampling_dates")
        dates.json_value = ["2016-01-01"]
        dates.save()
        run_aggregates()
        self.assertEqual(mock_validate_counties.call_count, 1)
        self.assertEqual(mock_update_dates.call_count, 1)
        self.assertEqual(NationalMortgageData.objects.count(), 1)
        self.assertEqual(StateMortgageData.objects.count(), 1)
        self.assertEqual(MSAMortgageData.objects.count(), 1)
        self.assertEqual(NonMSAMortgageData.objects.count(), 1)


class UpdateSamplingDatesTest(django.test.TestCase):
    fixtures = ["mortgage_constants.json", "mortgage_metadata.json"]

    def setUp(self):
        baker.make(
            CountyMortgageData,
            current=1250,
            date=datetime.date(2008, 1, 1),
            fips="12081",
            ninety=100,
            other=100,
            sixty=100,
            thirty=100,
            total=1650,
        )

    def test_update_sampling_dates(self):
        update_sampling_dates()
        self.assertEqual(
            MortgageMetaData.objects.get(name="sampling_dates").json_value,
            ["2008-01-01"],
        )


class DataScriptTest(django.test.TestCase):
    """Tests for data pipeline automations"""

    fixtures = ["mortgage_constants.json", "mortgage_metadata.json"]

    def test_validate_fips_too_short(self):
        fips_input = "12"
        self.assertEqual(validate_fips(fips_input), None)

    def test_validate_fips_too_long(self):
        fips_input = "123456"
        self.assertEqual(validate_fips(fips_input), None)

    def test_validate_fips_edge_case(self):
        fips_input = "46113"
        self.assertEqual(validate_fips(fips_input), "46102")

    def test_validate_fips_4_digit(self):
        fips_input = "1015"
        self.assertEqual(validate_fips(fips_input), "01015")

    def test_validate_fips_invalid_5_digit(self):
        fips_input = "02201"
        self.assertEqual(validate_fips(fips_input), None)

    def test_validate_fips_valid_5_digit(self):
        fips_input = "34041"
        self.assertEqual(validate_fips(fips_input), "34041")

    def test_validate_fips_outdated_fips(self):
        fips_input = "02201"  # a normally excluded outdated FIPS code
        self.assertIs(validate_fips(fips_input), None)

    def test_validate_fips_keep_outdated(self):
        fips_input = "02201"  # a normally excluded outdated FIPS code
        self.assertEqual(
            validate_fips(fips_input, keep_outdated=True), "02201"
        )


class ExportRoundingTests(unittest.TestCase):
    """Tests for rounding export values"""

    def test_round_pct_lessthan_1(self):
        value = 0.00781409295352325
        self.assertEqual(round_pct(value), 0.8)

    def test_round_pct_99(self):
        value = 0.98991409295352325
        self.assertEqual(round_pct(value), 99.0)

    def test_round_pct_greater_than_100(self):
        value = 1.00498991409295352325
        self.assertEqual(round_pct(value), 100.5)


class SaveMetadataTests(django.test.TestCase):
    def test_save_metadata(self):
        save_metadata(999, "slug1", "2017-01-01", "percent_90", "County")
        self.assertEqual(
            MortgageMetaData.objects.filter(name="download_files").count(), 1
        )
        save_metadata(9999, "slug2", "2017-02-01", "percent_90", "County")
        save_metadata(9999, "slug3", "2017-02-01", "percent_30_60", "County")
        updated_meta = MortgageMetaData.objects.get(name="download_files")
        data = updated_meta.json_value
        self.assertEqual(len(data), 2)


class BuildStateMsaDropdownTests(django.test.TestCase):
    fixtures = ["mortgage_constants.json", "geo_meta.json"]

    def setUp(self):
        self.states = {
            "10": {
                "fips": "10",
                "name": "Delaware",
                "abbr": "DE",
                "counties": ["10001", "10003", "10005"],
                "non_msa_counties": [],
                "msas": ["20100", "37980", "41540"],
                "non_msa_valid": False,
            },
            "15": {
                "fips": "15",
                "name": "Hawaii",
                "abbr": "HI",
                "counties": ["15001", "15003", "15005", "15007", "15009"],
                "non_msa_counties": ["15005"],
                "msas": ["27980", "46520"],
                "non_msa_valid": True,
            },
        }
        self.msas = {
            "27980": {
                "fips": "27980",
                "name": "Kahului-Wailuku-Lahaina, HI",
                "county_list": ["15005", "15007"],
            },
            "46520": {
                "fips": "46520",
                "name": "Urban Honolulu, HI",
                "county_list": ["15005", "15007"],
            },
        }
        self.counties = {
            "15005": {
                "fips": "15005",
                "name": "Kalawao County",
                "state": "HI",
            },
            "15007": {"fips": "15007", "name": "Kauai County", "state": "HI"},
        }

    def load_fips(self, mock_obj):
        mock_obj.state_fips = self.states
        mock_obj.msa_fips = self.msas
        mock_obj.county_fips = self.counties
        return mock_obj

    # @mock.patch(f"{DRS}.update_county_msa_meta.update_state_to_geo_meta")
    @mock.patch(f"{DRS}.update_county_msa_meta.FIPS")
    def test_update_msa_meta(self, mock_FIPS):  # mock_state_to_geo, ):
        mock_FIPS = self.load_fips(mock_FIPS)
        self.assertFalse(
            MortgageMetaData.objects.filter(name="state_msa_meta").exists()
        )
        update_state_to_geo_meta("msa")
        self.assertTrue(
            MortgageMetaData.objects.filter(name="state_msa_meta").exists()
        )
        test_json = MortgageMetaData.objects.get(
            name="state_msa_meta"
        ).json_value
        self.assertEqual(len(test_json), 2)

    @mock.patch(f"{DRS}.update_county_msa_meta.FIPS")
    @mock.patch(f"{DRS}.update_county_msa_meta.update_state_to_geo_meta")
    def test_update_county_meta(self, mock_state_to_geo, mock_FIPS):
        mock_FIPS = self.load_fips(mock_FIPS)
        self.assertFalse(
            MortgageMetaData.objects.filter(name="state_county_meta").exists()
        )
        update_state_to_geo_meta("county")
        test_json = MortgageMetaData.objects.get(
            name="state_county_meta"
        ).json_value
        self.assertEqual(len(test_json), 2)


class UpdateStateMsaDropdownTests(django.test.TestCase):
    fixtures = ["mortgage_constants.json", "mortgage_metadata.json"]

    @mock.patch(f"{DRS}.update_county_msa_meta.update_state_to_geo_meta")
    def test_run_rebuild(self, mock_update):
        run_update()
        self.assertEqual(mock_update.call_count, 2)
