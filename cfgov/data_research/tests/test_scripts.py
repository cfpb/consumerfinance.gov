from __future__ import unicode_literals

import datetime
import StringIO
import unittest

import django

import mock
import unicodecsv
from dateutil import parser
from mock import mock_open, patch
from model_mommy import mommy

from data_research.models import (
    County, CountyMortgageData, MetroArea, MortgageDataConstant,
    MortgageMetaData, MSAMortgageData, NationalMortgageData,
    NonMSAMortgageData, State, StateMortgageData, validate_counties
)
from data_research.mortgage_utilities.fips_meta import validate_fips
from data_research.mortgage_utilities.sql_utils import (
    assemble_insertions, chunk_entries
)
from data_research.scripts.export_public_csvs import (
    export_downloadable_csv, round_pct, row_starter, run as run_export,
    save_metadata
)
from data_research.scripts.load_mortgage_aggregates import (
    load_msa_values, load_national_values, load_non_msa_state_values,
    load_state_values, merge_the_dades, run as run_aggregates,
    update_sampling_dates
)
from data_research.scripts.load_mortgage_performance_csv import load_values
from data_research.scripts.source_to_dump import (
    convert_row_to_sql_tuple, create_dump, dump_as_csv, dump_as_sql,
    run as run_source_to_dump, update_through_date_constant
)
from data_research.scripts.update_county_msa_meta import (
    run as run_update, update_state_to_geo_meta
)


STARTING_DATE = datetime.date(2008, 1, 1)
THROUGH_DATE = datetime.date(2016, 12, 1)


class SourceToSQLTest(django.test.TestCase):

    date = datetime.date(2008, 1, 1)
    data_row = ['1', '01001', '2008-01-01', '1464',
                '1443', '10', '5', '4', '2', '2891']
    fixtures = ['mortgage_constants.json']

    def setUp(self):
        AL = mommy.make(
            State,
            fips='01',
            abbr='AL',
            name='Alabama')

        Autauga = mommy.make(
            County,
            id=2891,
            fips='01001',
            name='Autauga County',
            state=AL,
            valid=True)

        mommy.make(
            CountyMortgageData,
            fips='01001',
            date=self.date,
            total=1464,
            current=1443,
            thirty=10,
            sixty=5,
            ninety=4,
            other=2,
            county=Autauga)

    def test_convert_row_to_sql_tuple(self):
        expected = "(1,'01001','2008-01-01',1464,1443,10,5,4,2,2891)"
        entry = convert_row_to_sql_tuple(self.data_row)
        self.assertEqual(entry, expected)

    def test_chunk_entries(self):
        entries = [
            '1,01001,2008-01-01,1464,1443,10,5,4,2,2891',
            '2,01001,2008-01-01,1464,1443,10,5,4,2,2891',
            '3,01001,2008-01-01,1464,1443,10,5,4,2,2891',
            '4,01001,2008-01-01,1464,1443,10,5,4,2,2891'
        ]
        expected_chunks = [
            ['1,01001,2008-01-01,1464,1443,10,5,4,2,2891',
             '2,01001,2008-01-01,1464,1443,10,5,4,2,2891'],
            ['3,01001,2008-01-01,1464,1443,10,5,4,2,2891',
             '4,01001,2008-01-01,1464,1443,10,5,4,2,2891']
        ]
        chunk_generator = chunk_entries(entries, 2)
        self.assertEqual(
            [each for each in chunk_generator],
            expected_chunks)

    def test_update_thru_date(self):
        new_val = '2018-12-01'
        new_date = datetime.date(2018, 12, 1)
        update_through_date_constant(new_val)
        self.assertEqual(
            MortgageDataConstant.objects.get(name='through_date').date_value,
            new_date)

    def test_assemble_insertions(self):
        output = assemble_insertions(self.data_row)
        self.assertTrue(output.startswith('\n--\n--'))

    @mock.patch('data_research.scripts.'
                'source_to_dump.assemble_insertions')
    def test_dump_as_sql(self, mock_assemble):
        m = mock_open()
        with patch('__builtin__.open', m, create=True):
            dump_as_sql([self.data_row], '/tmp/mp_countydata')
        self.assertEqual(m.call_count, 1)
        self.assertEqual(mock_assemble.call_count, 1)

    def test_dump_as_csv(self):
        m = mock_open()
        with patch('__builtin__.open', m, create=True):
            dump_as_csv([self.data_row], '/tmp/mp_countydata')
        self.assertEqual(m.call_count, 1)

    @mock.patch('data_research.scripts.'
                'source_to_dump.create_dump')
    @mock.patch('data_research.scripts.'
                'source_to_dump.update_through_date_constant')
    def test_run_command(self, mock_update, mock_dump):
        run_source_to_dump('2017-03-01', '/tmp/mp_countydata')
        self.assertEqual(mock_update.call_count, 1)
        self.assertEqual(mock_dump.call_count, 1)

    @mock.patch('data_research.scripts.'
                'source_to_dump.create_dump')
    @mock.patch('data_research.scripts.source_to_dump.'
                'update_through_date_constant')
    def test_run_command_csv(self, mock_update, mock_dump):
        run_source_to_dump('2017-03-01', '/tmp/mp_countydata', 'csv')
        self.assertEqual(mock_update.call_count, 1)
        self.assertEqual(mock_dump.call_count, 1)

    @mock.patch('data_research.scripts.'
                'source_to_dump.create_dump')
    @mock.patch('data_research.scripts.source_to_dump.'
                'update_through_date_constant')
    def test_run_command_no_args(self, mock_update, mock_dump):
        run_source_to_dump()
        self.assertEqual(mock_update.call_count, 0)
        self.assertEqual(mock_dump.call_count, 0)

    @mock.patch('data_research.scripts.'
                'source_to_dump.read_in_s3_csv')
    @mock.patch('data_research.scripts.'
                'source_to_dump.dump_as_sql')
    def test_create_dump_sql(self, mock_dump_sql, mock_read_in):
        mock_read_in.return_value = [{
            'thirty': '4', 'month': '1', 'current': '262', 'sixty': '1',
            'ninety': '0', 'date': '01/01/2008', 'open': '270', 'other': '3',
            'fips': '01001'}]
        create_dump(STARTING_DATE, THROUGH_DATE, '/tmp/mp_countydata')
        self.assertEqual(mock_dump_sql.call_count, 1)
        self.assertEqual(mock_read_in.call_count, 1)

    @mock.patch('data_research.scripts.'
                'source_to_dump.read_in_s3_csv')
    @mock.patch('data_research.scripts.'
                'source_to_dump.dump_as_csv')
    def test_create_dump_csv(self, mock_dump_csv, mock_read_in):
        mock_read_in.return_value = [{
            'thirty': '4', 'month': '1', 'current': '262', 'sixty': '1',
            'ninety': '0', 'date': '01/01/2008', 'open': '270', 'other': '3',
            'fips': '01001'}]
        create_dump(
            STARTING_DATE, THROUGH_DATE, '/tmp/mp_countydata', sql=False)
        self.assertEqual(mock_dump_csv.call_count, 1)
        self.assertEqual(mock_read_in.call_count, 1)


class DataLoadIntegrityTest(django.test.TestCase):

    fixtures = ['mortgage_constants.json', 'mortgage_metadata.json']

    def setUp(self):

        FL = mommy.make(
            State,
            fips='12',
            abbr='FL',
            ap_abbr='Fla.',
            counties='["12081"]',
            msas='["52081"]',
            name='Florida',
            non_msa_counties='["12001"]',
            non_msa_valid=True)
        FL.save()

        mommy.make(
            County,
            fips='12081',
            name='Manatee County',
            state=FL,
            valid=True)

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
        'data_research.scripts.load_mortgage_performance_csv.'
        'read_in_s3_csv')
    def test_data_creation_from_base_row(
            self, mock_read_csv):
        """
        Confirm that loading a single row of real base data creates
        a CountyMortgageData object with the base row's values,
        and that the object's calculated API values are correct.
        """

        f = StringIO.StringIO(self.data_header + self.data_row)
        reader = unicodecsv.DictReader(f)
        mock_read_csv.return_value = reader
        load_values()
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

    def test_validate_counties(self):
        county = County.objects.first()
        self.assertIs(county.valid, True)
        validate_counties()
        county.refresh_from_db()
        self.assertIs(county.valid, False)


class MergeTheDadesTest(django.test.TestCase):

    fixtures = ['mortgage_constants.json', 'mortgage_metadata.json']

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

    fixtures = ['mortgage_constants.json', 'mortgage_metadata.json']

    def setUp(self):

        mommy.make(
            State,
            fips='12',
            abbr='FL',
            ap_abbr='Fla.',
            counties=["12081"],
            msas=["52081"],
            name='Florida',
            non_msa_counties=["12001"],
            non_msa_valid=True)

        mommy.make(
            County,
            fips='12081',
            name='Manatee County',
            state=State.objects.get(fips='12'),
            valid=True)

        mommy.make(
            MetroArea,
            fips='35840',
            name='North Port-Sarasota-Bradenton, FL',
            states=["12"],
            counties=["12081", "12115"],
            valid=True)

        mommy.make(
            CountyMortgageData,
            current=1250,
            date=datetime.date(2008, 1, 1),
            county=County.objects.get(fips='12081'),
            fips='12081',
            ninety=100,
            other=100,
            sixty=100,
            thirty=100,
            total=1650)

        mommy.make(
            MSAMortgageData,
            current=5250,
            date=datetime.date(2008, 1, 1),
            msa=MetroArea.objects.get(fips='35840'),
            fips='35840',
            ninety=1406,
            other=361,
            sixty=1275,
            thirty=3676,
            total=22674)

        mommy.make(
            NonMSAMortgageData,
            current=5250,
            date=datetime.date(2008, 1, 1),
            state=State.objects.get(fips='12'),
            fips='12-non',
            ninety=1406,
            other=361,
            sixty=1275,
            thirty=3676,
            total=22674)

        mommy.make(
            StateMortgageData,
            current=250081,
            date=datetime.date(2008, 1, 1),
            state=State.objects.get(fips='12'),
            fips='12',
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
            ninety=10000,
            other=10000,
            sixty=10000,
            thirty=10000,
            total=2540000)

    @mock.patch('data_research.scripts.export_public_csvs.bake_csv_to_s3')
    def test_export_downloadable_csv(self, mock_bake):
        run_export(prep_only=True)
        export_downloadable_csv('County', 'percent_30_60')
        self.assertEqual(mock_bake.call_count, 1)
        export_downloadable_csv('County', 'percent_90')
        self.assertEqual(mock_bake.call_count, 2)
        export_downloadable_csv('MetroArea', 'percent_30_60')
        self.assertEqual(mock_bake.call_count, 3)
        export_downloadable_csv('MetroArea', 'percent_90')
        self.assertEqual(mock_bake.call_count, 4)
        export_downloadable_csv('State', 'percent_30_60')
        self.assertEqual(mock_bake.call_count, 5)
        export_downloadable_csv('State', 'percent_90')
        self.assertEqual(mock_bake.call_count, 6)

    def test_row_starter(self):
        '''
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
        '''
        county_data = CountyMortgageData.objects.filter(fips='12081').first()
        county = county_data.county
        county_starter = row_starter('County', county_data)
        self.assertEqual(
            county_starter, ['County',
                             county.state.abbr,
                             county.name,
                             "'{}'".format(county_data.fips)])
        metro_data = MSAMortgageData.objects.filter(fips='35840').first()
        msa = metro_data.msa
        metro_starter = row_starter('MetroArea', metro_data)
        self.assertEqual(
            metro_starter, ['MetroArea',
                            msa.name,
                            metro_data.fips])
        state_data = StateMortgageData.objects.filter(fips='12').first()
        state = state_data.state
        state_starter = row_starter('State', state_data)
        self.assertEqual(
            state_starter, ['State',
                            state.name,
                            "'{}'".format(state_data.fips)])
        non_metro_data = NonMSAMortgageData.objects.get(fips='12-non')
        non_metro_starter = row_starter('NonMetroArea', non_metro_data)
        self.assertEqual(
            non_metro_starter, ['NonMetroArea',
                                non_metro_data.state.name,
                                non_metro_data.fips])


class RunExportTest(django.test.TestCase):
    """Tests the export runner."""

    fixtures = ['mortgage_constants.json', 'mortgage_metadata.json']

    @mock.patch(
        'data_research.scripts.export_public_csvs.export_downloadable_csv')
    def test_run_export(self, mock_export):
        run_export()
        self.assertEqual(mock_export.call_count, 6)


class DataLoadTest(django.test.TestCase):
    """Tests loading functions."""

    fixtures = ['mortgage_constants.json', 'mortgage_metadata.json']

    def setUp(self):

        FL = mommy.make(
            State,
            fips='12',
            abbr='FL',
            ap_abbr='Fla.',
            counties='["12081"]',
            msas='["52081"]',
            name='Florida',
            non_msa_counties='["12001"]',
            non_msa_valid=True)
        FL.save()

        manatee = mommy.make(
            County,
            fips='12081',
            name='Manatee County',
            state=FL,
            valid=True)
        manatee.save()

        mommy.make(
            MetroArea,
            fips='35840',
            name='North Port-Sarasota-Bradenton, FL',
            counties='["12081"]',
            states='["12"]',
            valid=True)

        mommy.make(
            CountyMortgageData,
            date=datetime.date(2016, 1, 1),
            fips='12081',
            county=manatee)

        mommy.make(
            MSAMortgageData,
            current=5250,
            date=datetime.date(2016, 1, 1),
            fips='35840',
            msa=MetroArea.objects.get(fips='35840'),
            ninety=1406,
            other=361,
            sixty=1275,
            thirty=3676,
            total=22674)

        mommy.make(
            NonMSAMortgageData,
            current=250081,
            date=datetime.date(2016, 1, 1),
            fips='12-non',
            state=State.objects.get(fips='12'),
            ninety=4069,
            other=3619,
            sixty=2758,
            thirty=6766,
            total=26748)

        mommy.make(
            StateMortgageData,
            current=250081,
            date=datetime.date(2016, 1, 1),
            state=State.objects.get(fips='12'),
            fips='12',
            ninety=4069,
            other=3619,
            sixty=2758,
            thirty=6766,
            total=26748)

    def test_update_through_date_constant(self):
        new_date = datetime.date(2016, 9, 1)
        update_through_date_constant(new_date)
        self.assertEqual(
            new_date,
            MortgageDataConstant.objects.get(name='through_date').date_value)

    def test_load_msa_values(self):
        self.assertEqual(MSAMortgageData.objects.count(), 1)
        load_msa_values('2009-12-01')
        self.assertEqual(MSAMortgageData.objects.count(), 2)

    def test_load_non_msa_state_values(self):
        self.assertEqual(State.objects.count(), 1)
        self.assertEqual(NonMSAMortgageData.objects.count(), 1)
        load_non_msa_state_values("2009-01-01")
        self.assertEqual(NonMSAMortgageData.objects.count(), 2)

    def test_load_state_values(self):
        load_state_values('2008-01-01')
        self.assertEqual(StateMortgageData.objects.count(), 2)

    def test_load_national_values(self):
        load_national_values('2016-09-01')
        self.assertEqual(NationalMortgageData.objects.count(), 1)
        load_national_values('2016-09-01')
        self.assertEqual(NationalMortgageData.objects.count(), 1)

    @mock.patch('data_research.scripts.'
                'load_mortgage_performance_csv.read_in_s3_csv')
    def test_load_values(self, mock_read_in):
        mock_read_in.return_value = [{
            'thirty': '4', 'month': '1', 'current': '262', 'sixty': '1',
            'ninety': '0', 'date': '01/01/2008', 'open': '270', 'other': '3',
            'fips': '12081'}]
        load_values()
        self.assertEqual(mock_read_in.call_count, 1)
        self.assertEqual(CountyMortgageData.objects.count(), 1)

    @mock.patch('data_research.scripts.'
                'load_mortgage_performance_csv.read_in_s3_csv')
    def test_load_values_return_fips(self, mock_read_in):
        mock_read_in.return_value = [{
            'thirty': '4', 'month': '1', 'current': '262', 'sixty': '1',
            'ninety': '0', 'date': '01/01/2008', 'open': '270', 'other': '3',
            'fips': '12081'}]
        fips_list = load_values(return_fips=True)
        self.assertEqual(mock_read_in.call_count, 1)
        self.assertEqual(fips_list, ['12081'])

    @mock.patch('data_research.scripts.'
                'load_mortgage_aggregates.update_sampling_dates')
    @mock.patch('data_research.scripts.'
                'load_mortgage_aggregates.validate_counties')
    def test_run_aggregates(self, mock_validate_counties, mock_update_dates):
        dates = MortgageMetaData.objects.get(
            name='sampling_dates')
        dates.json_value = ['2016-01-01']
        dates.save()
        run_aggregates()
        self.assertEqual(mock_validate_counties.call_count, 1)
        self.assertEqual(mock_update_dates.call_count, 1)
        self.assertEqual(NationalMortgageData.objects.count(), 1)
        self.assertEqual(StateMortgageData.objects.count(), 1)
        self.assertEqual(MSAMortgageData.objects.count(), 1)
        self.assertEqual(NonMSAMortgageData.objects.count(), 1)


class UpdateSamplingDatesTest(django.test.TestCase):

    fixtures = ['mortgage_constants.json', 'mortgage_metadata.json']

    def setUp(self):

        mommy.make(
            CountyMortgageData,
            current=1250,
            date=datetime.date(2008, 1, 1),
            fips='12081',
            ninety=100,
            other=100,
            sixty=100,
            thirty=100,
            total=1650)

    def test_update_sampling_dates(self):
        update_sampling_dates()
        self.assertEqual(
            MortgageMetaData.objects.get(
                name='sampling_dates').json_value,
            ['2008-01-01'])


class DataScriptTest(django.test.TestCase):
    """Tests for data pipeline automations"""

    fixtures = ['mortgage_constants.json', 'mortgage_metadata.json']

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
        save_metadata(999, 'slug1', '2017-01-01', 'percent_90', 'County')
        self.assertEqual(
            MortgageMetaData.objects.filter(name='download_files').count(), 1)
        save_metadata(9999, 'slug2', '2017-02-01', 'percent_90', 'County')
        save_metadata(9999, 'slug3', '2017-02-01', 'percent_30_60', 'County')
        updated_meta = MortgageMetaData.objects.get(name='download_files')
        data = updated_meta.json_value
        self.assertEqual(len(data), 2)


class BuildStateMsaDropdownTests(django.test.TestCase):

    fixtures = ['mortgage_constants.json']

    def setUp(self):
        self.states = {
            '10':
            {'AP': 'Del.',
             'fips': '10',
             'name': 'Delaware',
             'msa_counties': [],
             'non_msa_counties': [],
             'msas': [],
             'abbr': 'DE'},
            '15':
            {'AP': 'Hawaii',
             'fips': '15',
             'name': 'Hawaii',
             'msa_counties': ['15007'],
             'non_msa_counties': ['155005'],
             'msas': [],
             'abbr': 'HI'}
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
                'update_county_msa_meta.FIPS')
    def test_update_msa_meta(self, mock_FIPS):
        mock_FIPS = self.load_fips(mock_FIPS)
        self.assertFalse(
            MortgageMetaData.objects.filter(name='state_msa_meta').exists())
        update_state_to_geo_meta('msa')
        self.assertTrue(
            MortgageMetaData.objects.filter(name='state_msa_meta').exists())
        test_json = MortgageMetaData.objects.get(
            name='state_msa_meta').json_value
        self.assertEqual(len(test_json), 2)

    @mock.patch('data_research.scripts.'
                'update_county_msa_meta.FIPS')
    def test_update_county_meta(self, mock_FIPS):
        mock_FIPS = self.load_fips(mock_FIPS)
        self.assertFalse(
            MortgageMetaData.objects.filter(name='state_county_meta').exists())
        update_state_to_geo_meta('county')
        test_json = MortgageMetaData.objects.get(
            name='state_county_meta').json_value
        self.assertEqual(len(test_json), 2)


class UpdateStateMsaDropdownTests(django.test.TestCase):

    fixtures = ['mortgage_constants.json', 'mortgage_metadata.json']

    @mock.patch('data_research.scripts.'
                'update_county_msa_meta.update_state_to_geo_meta')
    def test_run_rebuild(self, mock_update):
        run_update()
        self.assertEqual(mock_update.call_count, 2)
