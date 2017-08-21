from __future__ import unicode_literals

import datetime
from dateutil import parser
import json
import mock
from mock import mock_open, patch
import StringIO
import unittest

import django.test
from model_mommy import mommy
import unicodecsv

from data_research.models import (
    CountyMortgageData,
    MortgageMetaData,
    MSAMortgageData,
    NationalMortgageData,
    StateMortgageData
)
from data_research.scripts.load_mortgage_performance_csv import (
    load_values,
    merge_the_dades,
    update_sampling_dates,
    validate_fips,
)
from data_research.scripts.load_mortgage_aggregates import (
    load_msa_values,
    load_national_values,
    load_state_values,
    run as run_aggregates)
from data_research.scripts.export_public_csv import (
    export_downloadable_csv,
    format_size,
    round_pct,
    run as run_export,
    save_metadata)
from data_research.scripts.update_county_msa_meta import (
    run as run_update,
    update_state_to_geo_meta)
from data_research.scripts.validate_geos import validate_geo


class ValidateGeoTest(django.test.TestCase):

    def test_validate_geo_no_records(self):
        test_value = validate_geo('county', '12081', 2016, 1000)
        self.assertIs(test_value, False)


class DataLoadIntegrityTest(django.test.TestCase):

    fixtures = ['mortgage_constants.json']

    def setUp(self):

        # real values from a base CSV row
        self.data_header = 'date,fips,open,current,thirty,sixty,ninety,other\n'
        self.data_row = '09/01/16,12081,1952,1905,21,5,10,11\n'
        self.data_row_dict = {'date': '09/01/16',
                              'fips': '12081',
                              'open': '1952',
                              'current': '1905',
                              'thirty': '21',
                              'sixty': '5',
                              'ninety': '10',
                              'other': '11'}

    @mock.patch(
        'data_research.scripts.load_mortgage_performance_csv.read_in_s3_csv')
    @mock.patch(
        'data_research.scripts.'
        'load_mortgage_performance_csv.update_sampling_dates')
    def test_data_creation_from_base_row(
            self, mock_update_dates, mock_read_csv):
        """
        Confirm that loading a single row of real base data creates
        a CountyMortgageData object with the base row's values,
        and that the object's calculated API values are correct.
        """

        f = StringIO.StringIO(self.data_header + self.data_row)
        reader = unicodecsv.DictReader(f)
        mock_read_csv.return_value = reader
        load_values('mock_s3_url')
        self.assertEqual(CountyMortgageData.objects.count(), 1)
        county = CountyMortgageData.objects.first()
        fields = reader.fieldnames
        fields.pop(fields.index('fips'))  # test string separately
        fields.pop(fields.index('open'))  # 'open' is stored as 'total'
        fields.pop(fields.index('date'))  # date must be parsed before testing
        self.assertEqual(county.fips, self.data_row_dict.get('fips'))
        open_value = int(self.data_row_dict.get('open'))
        self.assertEqual(county.total, open_value)
        target_date = parser.parse(self.data_row_dict['date']).date()
        self.assertEqual(county.date, target_date)
        for field in fields:  # remaining fields can be tested in a loop
            self.assertEqual(
                getattr(county, field), int(self.data_row_dict.get(field)))
        # test computed values
        self.assertEqual(
            county.epoch,
            int(target_date.strftime('%s')) * 1000)
        self.assertEqual(
            county.percent_90,
            int(self.data_row_dict.get('ninety')) * 1.0 / open_value)
        self.assertEqual(
            county.percent_30_60,
            (int(self.data_row_dict.get('thirty')) +
             int(self.data_row_dict.get('sixty'))) * 1.0 / open_value)


class AggregateLoadTest(django.test.TestCase):
    """Tests aggregate loading function"""

    fixtures = ['mortgage_constants.json']

    @mock.patch('data_research.scripts.'
                'load_mortgage_aggregates.load_fips_meta')
    def test_load_msa_values(self, mock_load_meta):
        from data_research.scripts.load_mortgage_aggregates import (
            FIPS, MSAMortgageData, load_msa_values)
        FIPS.msa_fips = {
            '45300':
            {'msa': 'Tampa-St. Petersburg-Clearwater, FL',
             'county_list': ['12081']}}
        date = "2016-09-01"
        load_msa_values(date)
        self.assertEqual(MSAMortgageData.objects.count(), 1)


class MergeTheDadesTest(django.test.TestCase):

    fixtures = ['mortgage_constants.json']

    def setUp(self):

        self.old_dade_fips = '12025'
        self.new_dade_fips = '12086'

        mommy.make(
            CountyMortgageData,
            current=100,
            date=datetime.date(2008, 1, 1),
            fips=self.old_dade_fips,
            ninety=100,
            other=100,
            sixty=100,
            thirty=100,
            total=500)

        mommy.make(
            CountyMortgageData,
            current=100,
            date=datetime.date(2008, 1, 1),
            fips=self.new_dade_fips,
            ninety=100,
            other=100,
            sixty=100,
            thirty=100,
            total=500)

    def test_merge_the_dades(self):
        merge_the_dades()
        new_dade = CountyMortgageData.objects.get(fips=self.new_dade_fips)
        for field in ['current', 'thirty', 'sixty', 'ninety', 'other']:
            self.assertEqual(getattr(new_dade, field), 200)
        self.assertEqual(new_dade.total, 1000)
        with self.assertRaises(CountyMortgageData.DoesNotExist):
            CountyMortgageData.objects.get(fips=self.old_dade_fips)
        # make sure a second run is idempotent
        merge_the_dades()
        for field in ['current', 'thirty', 'sixty', 'ninety', 'other']:
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

    fixtures = ['mortgage_constants.json']

    def setUp(self):

        mommy.make(
            CountyMortgageData,
            current=1250,
            date=datetime.date(2008, 1, 1),
            fips='12081',
            id=1,
            ninety=100,
            other=100,
            sixty=100,
            thirty=100,
            total=1650)

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
            StateMortgageData,
            current=250081,
            date=datetime.date(2008, 1, 1),
            fips='12',
            id=1,
            ninety=4069,
            other=3619,
            sixty=2758,
            thirty=6766,
            total=26748)

        mommy.make(
            NationalMortgageData,
            current=2500000,
            date=datetime.date(2008, 1, 1),
            fips='12',
            id=1,
            ninety=10000,
            other=10000,
            sixty=10000,
            thirty=10000,
            total=2540000)

    @mock.patch('data_research.scripts.export_public_csv.bake_csv_to_s3')
    def test_export_downloadable_csv(self, mock_bake):
        run_export(prep_only=True)
        export_downloadable_csv('County', 'percent_30_60')
        self.assertEqual(mock_bake.call_count, 1)
        export_downloadable_csv('MetroArea', 'percent_30_60')
        self.assertEqual(mock_bake.call_count, 2)
        export_downloadable_csv('State', 'percent_90')
        self.assertEqual(mock_bake.call_count, 3)


class RunExportTest(django.test.TestCase):
    """Tests the export runner."""

    fixtures = ['mortgage_constants.json']

    @mock.patch(
        'data_research.scripts.export_public_csv.export_downloadable_csv')
    def test_run_export(self, mock_export):
        run_export()
        self.assertEqual(mock_export.call_count, 6)


class DataLoadTest(django.test.TestCase):
    """Tests loading functions."""

    fixtures = ['mortgage_constants.json']

    def setUp(self):

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
            StateMortgageData,
            current=250081,
            date=datetime.date(2008, 1, 1),
            fips='12',
            id=1,
            ninety=4069,
            other=3619,
            sixty=2758,
            thirty=6766,
            total=26748)

    @mock.patch('data_research.scripts.load_mortgage_aggregates.'
                'MSAMortgageData.objects.get_or_create')
    @mock.patch('data_research.scripts.load_mortgage_aggregates.FIPS')
    def test_load_msa_values(self, mock_FIPS, mock_get_or_create):
        mock_FIPS.msa_fips = {'35840': {'county_list': ['12081']}}
        msa = MSAMortgageData.objects.first()
        mock_get_or_create.return_value = msa, False
        load_msa_values('2008-01-01')
        self.assertEqual(mock_get_or_create.call_count, 1)

    @mock.patch('data_research.scripts.load_mortgage_aggregates.'
                'StateMortgageData.objects.get_or_create')
    @mock.patch('data_research.scripts.load_mortgage_aggregates.FIPS')
    def test_load_state_values(self, mock_FIPS, mock_get_or_create):
        mock_FIPS.state_fips = {'12': ''}
        state = StateMortgageData.objects.first()
        mock_get_or_create.return_value = state, True
        load_state_values('2008-01-01')
        self.assertEqual(mock_get_or_create.call_count, 1)
        mock_get_or_create.return_value = state, False
        load_state_values('2008-01-01')
        self.assertEqual(mock_get_or_create.call_count, 2)

    def test_load_national_values(self):
        load_national_values('2016-09-01')
        self.assertEqual(NationalMortgageData.objects.count(), 1)
        load_national_values('2016-09-01')
        self.assertEqual(NationalMortgageData.objects.count(), 1)

    @mock.patch('data_research.scripts.'
                'load_mortgage_performance_csv.read_in_s3_csv')
    @mock.patch('data_research.scripts.'
                'load_mortgage_performance_csv.update_sampling_dates')
    @mock.patch('data_research.scripts.'
                'load_mortgage_performance_csv.merge_the_dades')
    def test_load_values(self, mock_dades, mock_update, mock_read_in):
        mock_read_in.return_value = [{
            'thirty': '4', 'month': '1', 'current': '262', 'sixty': '1',
            'ninety': '0', 'date': '01/01/98', 'open': '270', 'other': '3',
            'fips': '01001'}]
        load_values('mock_s3_url')
        self.assertEqual(mock_read_in.call_count, 1)
        self.assertEqual(mock_update.call_count, 1)
        self.assertEqual(mock_dades.call_count, 1)
        self.assertEqual(CountyMortgageData.objects.count(), 1)

    @mock.patch('data_research.scripts.'
                'load_mortgage_performance_csv.read_in_s3_csv')
    def test_load_values_return_fips(self, mock_read_in):
        mock_read_in.return_value = [{
            'thirty': '4', 'month': '1', 'current': '262', 'sixty': '1',
            'ninety': '0', 'date': '01/01/98', 'open': '270', 'other': '3',
            'fips': '01001'}]
        fips_list = load_values('mock_s3_url', return_fips=True)
        self.assertEqual(mock_read_in.call_count, 1)
        self.assertEqual(fips_list, ['01001'])


class UpdateSamplingDatesTest(django.test.TestCase):

    fixtures = ['mortgage_constants.json']

    def setUp(self):

        mommy.make(
            CountyMortgageData,
            current=1250,
            date=datetime.date(2008, 1, 1),
            fips='12081',
            id=1,
            ninety=100,
            other=100,
            sixty=100,
            thirty=100,
            total=1650)

    def test_update_sampling_dates(self):
        m = mock_open()
        with patch('__builtin__.open', m, create=True):
            update_sampling_dates()
        self.assertEqual(m.call_count, 1)
        self.assertEqual(
            MortgageMetaData.objects.get(
                name='sampling_dates').json_value,
            '["2008-01-01"]')


class DataScriptTest(unittest.TestCase):
    """Tests for data pipeline automations"""

    def test_format_size_bytes(self):
        self.assertEqual(format_size(999), '999.0B')

    def test_format_size_kilobytes(self):
        self.assertEqual(format_size(9999), '9.8KB')

    def test_format_size_megabytes(self):
        self.assertEqual(format_size(9999999), '9.5MB')

    def test_format_size_gigabytes(self):
        self.assertEqual(format_size(9999999999), '9.3GB')

    def test_format_size_terabytes(self):
        self.assertEqual(format_size(9999999999999), '9.1TB')

    def test_validate_fips_too_short(self):
        fips_input = '12'
        self.assertEqual(validate_fips(fips_input), None)

    def test_validate_fips_too_long(self):
        fips_input = '123456'
        self.assertEqual(validate_fips(fips_input), None)

    def test_validate_fips_edge_case(self):
        fips_input = '46113'
        self.assertEqual(validate_fips(fips_input), '46102')

    def test_validate_fips_4_digit(self):
        fips_input = '1015'
        self.assertEqual(validate_fips(fips_input), '01015')

    def test_validate_fips_invalid_5_digit(self):
        fips_input = '02201'
        self.assertEqual(validate_fips(fips_input), None)

    def test_validate_fips_valid_5_digit(self):
        fips_input = '34041'
        self.assertEqual(validate_fips(fips_input), '34041')

    def test_validate_fips_outdated_fips(self):
        fips_input = '02201'  # a normally excluded outdated FIPS code
        self.assertIs(validate_fips(fips_input), None)

    def test_validate_fips_keep_outdated(self):
        fips_input = '02201'  # a normally excluded outdated FIPS code
        self.assertEqual(validate_fips(
            fips_input, keep_outdated=True), '02201')

    @mock.patch('data_research.scripts.'
                'load_mortgage_aggregates.load_fips_meta')
    @mock.patch('data_research.scripts.'
                'load_mortgage_aggregates.load_msa_values')
    @mock.patch('data_research.scripts.'
                'load_mortgage_aggregates.load_state_values')
    @mock.patch('data_research.scripts.'
                'load_mortgage_aggregates.load_national_values')
    def test_run_aggregates(self, mock_load_national, mock_load_states,
                            mock_load_msas, mock_load_fips):
        from data_research.scripts.load_mortgage_aggregates import FIPS
        FIPS.dates = ['2016-09-01']
        run_aggregates()
        self.assertEqual(mock_load_fips.call_count, 1)
        self.assertEqual(mock_load_national.call_count, 1)
        self.assertEqual(mock_load_states.call_count, 1)
        self.assertEqual(mock_load_msas.call_count, 1)

    @mock.patch('data_research.scripts.'
                'load_mortgage_performance_csv.load_values')
    def test_run_csv_load(self, mock_load):
        from data_research.scripts import load_mortgage_performance_csv
        load_mortgage_performance_csv.run('fake_slug')
        self.assertEqual(mock_load.call_count, 1)


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
        save_metadata(999, 'slug1', '2017-01-01')
        self.assertEqual(
            MortgageMetaData.objects.filter(name='download_files').count(), 1)
        save_metadata(9999, 'slug2', '2017-02-01')
        updated_meta = MortgageMetaData.objects.get(name='download_files')
        data = json.loads(updated_meta.json_value)
        self.assertEqual(len(data), 2)


class BuildStateMsaDropdownTests(django.test.TestCase):

    fixtures = ['mortgage_constants.json']

    def setUp(self):
        self.states = {
            '10':
            {'AP': 'Del.', 'fips': '10', 'name': 'Delaware', 'abbr': 'DE'},
            '15':
            {'AP': 'Hawaii', 'fips': '15', 'name': 'Hawaii', 'abbr': 'HI'}
        }
        self.msas = {
            "27980": {
                "fips": "27980",
                "name": "Kahului-Wailuku-Lahaina, HI",
                "county_list": ['15005', '15007'],
            },
            "46520": {
                "fips": "46520",
                "name": "Urban Honolulu, HI",
                "county_list": ['15005', '15007'],
            }
        }
        self.counties = {
            "15005": {
                "fips": "15005",
                "name": "Kalawao County",
                "state": "HI"
            },
            "15007": {
                "fips": "15007",
                "name": "Kauai County",
                "state": "HI"
            }
        }

    def load_fips(self, mock_obj):
        mock_obj.state_fips = self.states
        mock_obj.msa_fips = self.msas
        mock_obj.county_fips = self.counties
        return mock_obj

    @mock.patch('data_research.scripts.'
                'update_county_msa_meta.bake_json_to_s3')
    @mock.patch('data_research.scripts.'
                'update_county_msa_meta.FIPS')
    def test_update_msa_meta(self, mock_FIPS, mock_bake_s3):
        mock_FIPS = self.load_fips(mock_FIPS)
        self.assertFalse(
            MortgageMetaData.objects.filter(name='state_msa_meta').exists())
        update_state_to_geo_meta('msa')
        self.assertTrue(
            MortgageMetaData.objects.filter(name='state_msa_meta').exists())
        self.assertEqual(mock_bake_s3.call_count, 1)
        test_json = json.loads(
            MortgageMetaData.objects.get(name='state_msa_meta').json_value)
        self.assertEqual(len(test_json), 2)

    @mock.patch('data_research.scripts.'
                'update_county_msa_meta.bake_json_to_s3')
    @mock.patch('data_research.scripts.'
                'update_county_msa_meta.FIPS')
    def test_update_county_meta(self, mock_FIPS, mock_bake_s3):
        mock_FIPS = self.load_fips(mock_FIPS)
        self.assertFalse(
            MortgageMetaData.objects.filter(name='state_county_meta').exists())
        update_state_to_geo_meta('county')
        self.assertEqual(mock_bake_s3.call_count, 1)
        test_json = json.loads(
            MortgageMetaData.objects.get(name='state_county_meta').json_value)
        self.assertEqual(len(test_json), 2)

    @mock.patch('data_research.scripts.'
                'update_county_msa_meta.update_state_to_geo_meta')
    def test_run_rebuild(self, mock_update):
        run_update()
        self.assertEqual(mock_update.call_count, 2)
