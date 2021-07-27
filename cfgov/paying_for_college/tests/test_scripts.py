import copy
import datetime
import json
import unittest
from decimal import Decimal
from unittest import mock
from unittest.mock import mock_open, patch

import django
from django.conf import settings
from django.db import connection
from django.utils import timezone

import requests
from requests.exceptions import SSLError

from paying_for_college.disclosures.scripts import (
    api_utils, nat_stats, notifications, process_cohorts, purge_objects,
    tag_settlement_schools, update_colleges, update_ipeds
)
from paying_for_college.disclosures.scripts.notification_tester import (
    send_test_notifications
)
from paying_for_college.models import (
    FAKE_SCHOOL_PKS, Alias, Notification, Program, School
)


COLLEGE_ROOT = "{}/paying_for_college".format(settings.PROJECT_ROOT)


class ProgamDataTest(django.test.TestCase):
    """Test the program data checks and creation."""

    fixtures = ['fake_school.json', 'test_fixture.json']

    def setUp(self):
        stdout_patch = mock.patch('sys.stdout')
        stdout_patch.start()
        self.addCleanup(stdout_patch.stop)
        self.mock_program_data = {
            'earnings': {
                'median_earnings': 3000
            },
            'debt': {
                'median_debt': 20000,
                'monthly_debt_payment': 400
            },
            'credential': {
                'level': '5'
            },
            'code': '5101',
            'title': 'Nursing',
            'counts': {
                'titleiv': 3000
            },

        }
        self.empty_mock_program_data = {
            'earnings': {
                'median_earnings': None
            },
            'debt': {
                'median_debt': None,
                'montly_debt_payent': None
            }
        }
        self.school = School.objects.get(pk=999999)

    def test_single_school_failure(self):
        (flist, msg) = update_colleges.update(single_school=99999)
        self.assertIn("Could not find", msg)

    def test_program_data_check_passes(self):
        self.assertTrue(
            update_colleges.test_for_program_data(
                self.mock_program_data))

    def test_empty_program_data_fails(self):
        self.assertFalse(
            update_colleges.test_for_program_data(
                self.empty_mock_program_data))

    def test_program_creation_empty_data(self):
        """Check that update_programs bails when there's no data."""
        empty_program_data = {
            'latest.programs.cip_4_digit': [self.empty_mock_program_data]
        }
        count = update_colleges.update_programs(
            empty_program_data, self.school)
        self.assertEqual(count, 0)

    def test_program_creation_success(self):
        """Check the update_programs succeeds with good data."""
        api_data = {
            'latest.programs.cip_4_digit': [self.mock_program_data]
        }
        count = update_colleges.update_programs(api_data, self.school)
        self.assertEqual(count, 1)
        self.assertTrue(Program.objects.filter(
            institution=self.school,
            program_code='5101-5').exists())

    @patch('paying_for_college.disclosures.scripts.update_colleges.get_scorecard_data')  # noqa
    def test_store_programs(self, mock_get_data):
        api_data = {'latest.programs.cip_4_digit': [self.mock_program_data]}
        mock_get_data.return_value = api_data
        test_pk = 100636
        program_count = Program.objects.count()
        (NO_DATA, endmsg) = update_colleges.update(
            single_school=test_pk, store_programs=True)
        self.assertEqual(Program.objects.count(), program_count + 1)


class TaggingTests(django.test.TestCase):
    """Test functions for tagging settlement schools via CSV."""

    fixtures = ['test_fixture.json']
    mock_csv_data = [{"ipeds_unit_id": "243197",
                      "flag": "mock_university"}]
    bad_csv_data = [{"ipeds_unit_id": "243197",
                     "floog": "mock_university"}]

    @mock.patch('paying_for_college.disclosures.scripts.'
                'tag_settlement_schools.read_in_s3')
    def test_tag_schools(self, mock_read_in):
        mock_read_in.return_value = self.mock_csv_data
        msg = tag_settlement_schools.tag_schools('mock_s3URL')
        self.assertIn("mock_university", msg)
        self.assertIn("tagged as", msg)
        flagged = School.objects.filter(settlement_school='mock_university')
        self.assertTrue(flagged.count() == 1)

    @mock.patch('paying_for_college.disclosures.scripts.'
                'tag_settlement_schools.read_in_s3')
    def test_tag_schools_no_data(self, mock_read_in):
        mock_read_in.return_value = [{}]
        msg = tag_settlement_schools.tag_schools('mock_s3URL')
        self.assertIn("ERROR", msg)

    @mock.patch('paying_for_college.disclosures.scripts.'
                'tag_settlement_schools.read_in_s3')
    def test_tag_schools_bad_heading(self, mock_read_in):
        mock_read_in.return_value = self.bad_csv_data
        msg = tag_settlement_schools.tag_schools('mock_s3URL')
        self.assertIn("ERROR", msg)


class PurgeTests(django.test.TestCase):

    fixtures = ['test_fixture.json', 'test_program.json']

    def test_purges(self):
        self.assertTrue(Program.objects.exists())
        self.assertTrue(Notification.objects.exists())
        self.assertEqual(
            purge_objects.purge('schools'), purge_objects.error_msg)
        self.assertEqual(
            purge_objects.purge(''), purge_objects.no_args_msg)
        self.assertIn("test-programs", purge_objects.purge('test-programs'))
        self.assertTrue(Program.objects.exists())
        self.assertIn("programs", purge_objects.purge('programs'))
        self.assertFalse(Program.objects.exists())
        self.assertIn("notifications", purge_objects.purge('notifications'))
        self.assertFalse(Notification.objects.exists())


class TestScripts(django.test.TestCase):

    fixtures = ['test_fixture.json', 'test_contacts.json']
    api_fixture = '{}/fixtures/sample_4yr_api_result.json'.format(COLLEGE_ROOT)

    # a full sample API return for a 4-year school (Texas Tech 229115)
    with open(api_fixture, 'r') as f:
        mock_results = json.loads(f.read())

    # a partial sample API return for a community college
    mock_lt_4 = {
        'results': [{
            'id': 100636,
            'ope6_id': '011667',
            'latest.student.size': 2693,
            'school.accreditor': "Higher Learning Commission",
            'school.degrees_awarded.predominant': 2,
            'school.degrees_awarded.highest': 2,
            'school.ownership': 1,
            'latest.completion.completion_rate_4yr_150nt_pooled': None,
            'latest.completion.completion_rate_less_than_4yr_150nt_pooled': 0.541,  # noqa
            'latest.academics.program_percentage.humanities': 0.5623,
            'latest.academics.program_percentage.agriculture': 0.200,
            'latest.academics.program_percentage.physical_science': 0.0900,
            'latest.academics.program_percentage.biological': 0.100,
            'school.main_campus': True,
            'school.online_only': False,
            'school.operating': False,
            'school.under_investigation': False,
            'school.city': 'Norfolk',
            'school.state': 'NE',
        }],
        'metadata': {'page': 0}
    }
    no_data_dict = {'results': []}
    mock_results2 = {
        'results': [{
            'id': 408039,
            'key': 'value'}],
        'metadata': {'page': 0}
    }

    def setUp(self):
        for method in ('print', 'sys.stdout'):
            base = 'paying_for_college.disclosures.scripts.update_colleges.'
            patcher = patch(base + method)
            patcher.start()
            self.addCleanup(patcher.stop)

    def test_get_grad_level(self):
        """Make sure higher-degree schools join the grad-degree '4' cohort."""
        level_2_school = School.objects.get(pk=100636)
        level_4_school = School.objects.get(pk=243197)
        level_5_school = School.objects.get(pk=243197)
        self.assertEqual(
            process_cohorts.get_grad_level(level_2_school), '2'
        )
        self.assertEqual(
            process_cohorts.get_grad_level(level_4_school), '4'
        )
        self.assertEqual(
            process_cohorts.get_grad_level(level_5_school), '4'
        )

    def test_school_with_no_degrees_highest(self):
        """A school with no degrees_highest value should not be in a cohort."""
        school_pk = 155555
        self.assertEqual(School.objects.get(pk=school_pk).degrees_highest, '')
        process_cohorts.run(single_school=school_pk)
        self.assertIs(
            School.objects.get(pk=school_pk).cohort_ranking_by_highest_degree,
            None
        )

    def test_build_base_cohorts(self):
        school = School.objects.get(pk=100654)
        base_query = process_cohorts.build_base_cohorts()
        cohort = process_cohorts.DEGREE_COHORTS.get(school.degrees_highest)
        metric = 'grad_rate'
        self.assertEqual(
            base_query.count(), 6)
        self.assertEqual(
            process_cohorts.rank_by_metric(school, cohort, metric).get(
                'percentile_rank'),
            80
        )

    def test_percentile_rank_blank_array(self):
        self.assertIs(
            process_cohorts.calculate_percentile_rank([], 0.50),
            None
        )

    @unittest.skipUnless(
        connection.vendor == 'postgresql', 'PostgreSQL-dependent')
    def test_run_cohorts(self):
        school = School.objects.get(pk=100654)
        self.assertIs(
            school.cohort_ranking_by_state,
            None
        )
        process_cohorts.run()
        school.refresh_from_db()
        self.assertEqual(
            type(school.cohort_ranking_by_state),
            dict
        )
        self.assertEqual(
            school.cohort_ranking_by_state.get(
                'grad_rate').get('percentile_rank'),
            100
        )

    @unittest.skipUnless(
        connection.vendor == 'postgresql', 'PostgreSQL-dependent')
    def test_run_cohorts_singleton(self):
        school = School.objects.get(pk=100654)
        self.assertIs(
            school.cohort_ranking_by_state,
            None
        )
        process_cohorts.run(single_school=100654)
        school.refresh_from_db()
        self.assertEqual(
            school.cohort_ranking_by_state.get(
                'grad_rate').get('percentile_rank'),
            100
        )

    def test_icomma(self):
        icomma_test = update_ipeds.icomma(445999)
        self.assertTrue(icomma_test == '445,999')

    def test_fix_zip5(self):
        fixzip3 = update_colleges.fix_zip5('501')
        self.assertTrue(fixzip3 == '00501')
        fixzip4 = update_colleges.fix_zip5('5501')
        self.assertTrue(fixzip4 == '05501')
        testzip5 = update_colleges.fix_zip5('55105')
        self.assertTrue(testzip5 == '55105')

    def test_set_school_grad_rate_4yr(self):
        school = School.objects.get(pk=100654)
        api_data = {
            'latest.completion.completion_rate_4yr_150nt_pooled': 0.44,
            'latest.completion.completion_rate_less_than_4yr_150nt_pooled': None,  # noqa
        }
        school = update_colleges.set_school_grad_rate(school, api_data)
        self.assertEqual(school.grad_rate, Decimal('0.44'))
        self.assertEqual(school.grad_rate_4yr, Decimal('0.44'))
        self.assertEqual(school.grad_rate_lt4, None)

    def test_set_school_grad_rate_lt4(self):
        school = School.objects.get(pk=100636)
        api_data = {
            'latest.completion.completion_rate_4yr_150nt_pooled': None,
            'latest.completion.completion_rate_less_than_4yr_150nt_pooled': 0.54,  # noqa
        }
        school = update_colleges.set_school_grad_rate(school, api_data)
        self.assertEqual(school.grad_rate, Decimal('0.54'))
        self.assertEqual(school.grad_rate_lt4, Decimal('0.54'))
        self.assertEqual(school.grad_rate_4yr, None)

    @unittest.skipUnless(
        connection.vendor == 'postgresql', 'PostgreSQL-dependent')
    @patch(
        'paying_for_college.disclosures.scripts.update_colleges.requests.get')
    def test_api_school_query(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_results
        mock_response.ok = True
        mock_requests.return_value = mock_response
        api_utils.api_school_query(123456, 'school.name')
        self.assertEqual(mock_requests.call_count, 1)
        self.assertTrue(mock_requests.called_with((123456, 'school.name')))

    @unittest.skipUnless(
        connection.vendor == 'postgresql', 'PostgreSQL-dependent')
    @patch('paying_for_college.disclosures.scripts.update_colleges.get_scorecard_data')  # noqa
    def test_single_school_request(self, mock_get_data):
        mock_get_data.return_value = self.mock_results.get('results')[0]
        update_colleges.update(single_school=408039)
        self.assertEqual(mock_get_data.call_count, 1)
        self.assertTrue(mock_get_data.called_with(
            408039,
            api_utils.build_field_string()
        ))

    @patch('paying_for_college.disclosures.scripts.update_colleges.get_scorecard_data')  # noqa
    def test_update_colleges_success(self, mock_get_data):
        mock_get_data.return_value = self.mock_results.get('results')[0]
        (NO_DATA, endmsg) = update_colleges.update()
        self.assertTrue(len(NO_DATA) == 0)
        self.assertTrue('Updated' in endmsg)

    @patch('paying_for_college.disclosures.scripts.update_colleges.get_scorecard_data')  # noqa
    def test_update_colleges_success_community_college(self, mock_get_data):
        mock_get_data.return_value = self.mock_lt_4.get('results')[0]
        (NO_DATA, endmsg) = update_colleges.update(
            single_school=100636)
        self.assertTrue(len(NO_DATA) == 0)
        self.assertTrue('Updated' in endmsg)

    @patch('paying_for_college.disclosures.scripts.update_colleges.get_scorecard_data')  # noqa
    def test_update_colleges_single_not_operating(self, mock_get_data):
        altered_results = copy.copy(self.mock_results).get('results')[0]
        altered_results['school.operating'] = 0
        mock_get_data.return_value = altered_results
        (NO_DATA, endmsg) = update_colleges.update(
            single_school=408039)
        self.assertTrue(len(NO_DATA) == 0)
        self.assertTrue('closed since last run: 1' in endmsg)

    @patch('paying_for_college.disclosures.scripts.update_colleges.get_scorecard_data')  # noqa
    def test_update_colleges_no_data_single_school(self, mock_get_data):
        mock_get_data.return_value = None
        (NO_DATA, endmsg) = update_colleges.update(
            single_school=408039)
        self.assertEqual(len(NO_DATA), 1)

    @patch('paying_for_college.disclosures.scripts.update_colleges.get_scorecard_data')  # noqa
    def test_update_colleges_community_colleges(self, mock_get_data):
        mock_get_data.return_value = self.mock_lt_4.get('results')[0]
        (NO_DATA, endmsg) = update_colleges.update()
        self.assertTrue(len(NO_DATA) == 0)

    @patch('paying_for_college.disclosures.scripts.update_colleges.get_scorecard_data')  # noqa
    def test_update_colleges_no_data(self, mock_get_data):
        mock_get_data.return_value = None
        update_colleges.update()
        self.assertEqual(
            mock_get_data.call_count,
            School.objects.filter(operating=True).exclude(
                pk__in=FAKE_SCHOOL_PKS).count())

    def check_compile_net_prices(self, control):
        mock_api_data = self.mock_results.get('results')[0]
        mock_avg_net_price = mock_api_data.get(
            'latest.cost.avg_net_price.%s' % control.lower())
        school, _ = School.objects.get_or_create(school_id=229115)
        school.control = control
        school = update_colleges.compile_net_prices(school, mock_api_data)
        self.assertEqual(school.avg_net_price, mock_avg_net_price)
        for each in ['0_30k', '30k_48k', '48k_75k', '75k_110k', '110k_plus']:
            self.assertIn(each, school.avg_net_price_slices.keys())

    @unittest.skipUnless(
        connection.vendor == 'postgresql', 'PostgreSQL-dependent')
    def test_compile_net_prices_public(self):
        self.check_compile_net_prices('Public')

    @unittest.skipUnless(
        connection.vendor == 'postgresql', 'PostgreSQL-dependent')
    def test_compile_net_prices_private(self):
        self.check_compile_net_prices('Private')

    @patch(
        'paying_for_college.disclosures.scripts.update_colleges.requests.get')
    def test_get_scorecard_data(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_results
        mock_response.ok = True
        mock_requests.return_value = mock_response
        data = update_colleges.get_scorecard_data('example.com')
        self.assertEqual(mock_requests.call_count, 1)
        self.assertTrue(mock_requests.called_with('example.com'))
        self.assertEqual(type(data), dict)

    @patch(
        'paying_for_college.disclosures.scripts.update_colleges.requests.get',
        side_effect=SSLError
    )
    def test_get_scorecard_data_ssl_error(self, mock_requests):
        test_data = update_colleges.get_scorecard_data('example.com')
        self.assertEqual(mock_requests.call_count, 1)
        self.assertIsNone(test_data)

    @patch(
        'paying_for_college.disclosures.scripts.update_colleges.requests.get')
    def test_get_scorecard_data_throttled(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.ok = False
        mock_response.reason = "API limit reached"
        mock_response.status_code = 429
        mock_requests.return_value = mock_response
        test_data = update_colleges.get_scorecard_data('example.com')
        self.assertEqual(mock_requests.call_count, 1)
        self.assertIs(test_data, None)

    @patch(
        'paying_for_college.disclosures.scripts.update_colleges.requests.get')
    def test_get_scorecard_data_no_results(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.ok = True
        mock_response.json.return_value = self.no_data_dict
        mock_requests.return_value = mock_response
        test_data = update_colleges.get_scorecard_data('example.com')
        self.assertEqual(mock_requests.call_count, 1)
        self.assertIs(test_data, None)

    def test_create_alias(self):
        update_ipeds.create_alias('xyz', School.objects.first())
        self.assertTrue(Alias.objects.get(alias='xyz'))

    @patch('paying_for_college.disclosures.scripts.update_ipeds.create_alias')
    def test_create_school(self, mock_create_alias):
        update_ipeds.create_school('999998', {'alias': 'xyzz', 'city': 'Oz'})
        self.assertTrue(mock_create_alias.call_count == 1)
        self.assertTrue(School.objects.get(school_id=999998))

    @patch(
        'paying_for_college.disclosures.scripts.update_ipeds.process_datafiles')  # noqa
    @patch('paying_for_college.disclosures.scripts.update_ipeds.dump_csv')
    @patch('paying_for_college.disclosures.scripts.update_ipeds.create_school')
    def test_process_missing(
            self, mock_create_school, mock_dump, mock_process_datafiles):
        mock_process_datafiles.return_value = {
            '999998': {'onCampusAvail': 'yes'}}
        update_ipeds.process_missing(['999998'])
        self.assertTrue(mock_dump.call_count == 1)
        self.assertTrue(mock_create_school.call_count == 1)
        self.assertTrue(mock_process_datafiles.call_count == 1)

    def test_dump_csv(self):
        m = mock_open()
        with patch("builtins.open", m, create=True):
            update_ipeds.dump_csv(
                '/tmp/mockfile.csv',
                ['a', 'b', 'c'],
                [{'a': 'd', 'b': 'e', 'c': 'f'}])

        self.assertTrue(m.call_count == 1)

    def test_write_clean_csv(self):
        m = mock_open()
        with patch("builtins.open", m, create=True):
            update_ipeds.write_clean_csv(
                '/tmp/mockfile.csv',
                ['a ', ' b', ' c '],
                ['a', 'b', 'c'],
                [{'a ': 'd', ' b': 'e', ' c ': 'f'}])
        self.assertTrue(m.call_count == 1)

    @patch(
        'paying_for_college.disclosures.scripts.update_ipeds.download_files')
    def test_read_csv(self, mock_download):
        m = mock_open(read_data='a , b, c \nd,e,f')
        with patch("builtins.open", m):
            fieldnames, data = update_ipeds.read_csv('mockfile.csv')
        self.assertEqual(mock_download.call_count, 1)
        self.assertEqual(m.call_count, 1)
        # self.assertEqual(fieldnames, ['a ', ' b', ' c '])
        # self.assertEqual(data, [{'a ': 'd', ' b': 'e', ' c ': 'f'}])

    @patch('paying_for_college.disclosures.scripts.update_ipeds.read_csv')
    @patch(
        'paying_for_college.disclosures.scripts.update_ipeds.write_clean_csv')
    def test_clean_csv_headings(self, mock_write, mock_read):
        mock_read.return_value = (['UNITID', 'PEO1ISTR'],
                                  {'UNITID': '100654', 'PEO1ISTR': '0'})
        update_ipeds.clean_csv_headings()
        self.assertEqual(mock_read.call_count, 3)
        self.assertEqual(mock_write.call_count, 3)

    def test_unzip_file(self):
        test_zip = ('{}/data_sources/ipeds/'
                    'test.txt.zip'.format(COLLEGE_ROOT))
        self.assertTrue(update_ipeds.unzip_file(test_zip))

    @patch('paying_for_college.disclosures.scripts.update_ipeds.requests.get')
    @patch('paying_for_college.disclosures.scripts.update_ipeds.unzip_file')
    @patch('paying_for_college.disclosures.scripts.update_ipeds.call')
    def test_download_zip_file(self, mock_call, mock_unzip, mock_requests):
        mock_response = mock.Mock()
        mock_response.ok = False
        mock_requests.return_value = mock_response
        down1 = update_ipeds.download_zip_file('fake.zip', '/tmp/fakefile.zip')
        self.assertFalse(down1)
        mock_response2 = mock.MagicMock()
        mock_response2.iter_content(chunk_size=None).return_value = ['a', 'b']
        mock_response2.ok = True
        mock_requests.return_value = mock_response2
        down2 = update_ipeds.download_zip_file('fake.zip', '/tmp/fakefile.zip')
        self.assertTrue(mock_unzip.call_count == 1)
        self.assertTrue(mock_call.call_count == 1)
        self.assertTrue(down2)

    @patch(
        'paying_for_college.disclosures.scripts.update_ipeds.download_zip_file')  # noqa
    @patch(
        'paying_for_college.disclosures.scripts.update_ipeds.clean_csv_headings')  # noqa
    def test_download_files(self, mock_clean, mock_download_zip):
        mock_download_zip.return_value = True
        update_ipeds.download_files()
        self.assertTrue(mock_download_zip.call_count == 3)
        self.assertTrue(mock_clean.call_count == 1)
        mock_download_zip.return_value = False
        update_ipeds.download_files()
        self.assertTrue(mock_download_zip.call_count == 6)
        self.assertTrue(mock_clean.call_count == 2)

    @patch('paying_for_college.disclosures.scripts.update_ipeds.read_csv')
    def test_process_datafiles(self, mock_read):
        points = update_ipeds.DATA_POINTS
        school_points = update_ipeds.NEW_SCHOOL_DATA_POINTS
        mock_return_dict = {points[key]: 'x' for key in points}
        mock_return_dict['UNITID'] = '999999'
        mock_return_dict['ROOM'] = '1'
        mock_fieldnames = ['UNITID', 'ROOM'] + list(points.keys())
        mock_read.return_value = (mock_fieldnames, [mock_return_dict])
        mock_results = update_ipeds.process_datafiles()
        self.assertTrue(mock_read.call_count == 2)
        self.assertTrue('999999' in mock_results.keys())
        mock_fieldnames = ['UNITID'] + list(school_points.keys())
        mock_return_dict = {school_points[key]: 'x' for key in school_points}
        mock_return_dict['UNITID'] = '999999'
        mock_read.return_value = (mock_fieldnames, [mock_return_dict])
        mock_results = update_ipeds.process_datafiles(add_schools=['999999'])
        self.assertTrue(mock_read.call_count == 3)

    @patch(
        'paying_for_college.disclosures.scripts.update_ipeds.process_datafiles')  # noqa
    @patch(
        'paying_for_college.disclosures.scripts.update_ipeds.process_missing')
    def test_load_values(self, mock_process_missing, mock_process):
        mock_process.return_value = {'999999': {'onCampusAvail': '2'}}
        msg = update_ipeds.load_values()
        self.assertTrue('DRY' in msg)
        self.assertTrue(mock_process.call_count == 1)
        mock_process.return_value = {'243197': {'onCampusAvail': '2',
                                                'books': '.'}}
        msg = update_ipeds.load_values()
        self.assertTrue('DRY' in msg)
        self.assertTrue(mock_process.call_count == 2)
        msg = update_ipeds.load_values(dry_run=False)
        self.assertFalse('DRY' in msg)
        self.assertTrue(mock_process.call_count == 3)
        mock_process.return_value = {'243197': {'onCampusAvail': '1'}}
        msg = update_ipeds.load_values()
        self.assertTrue('DRY' in msg)
        self.assertTrue(mock_process.call_count == 4)
        mock_process.return_value = {'999998': {'onCampusAvail': '2'}}
        msg = update_ipeds.load_values(dry_run=False)
        self.assertFalse('DRY' in msg)
        self.assertTrue(mock_process.call_count == 5)
        self.assertTrue(mock_process_missing.call_count == 1)

    @patch('paying_for_college.disclosures.scripts.notifications.send_mail')
    def test_send_stale_notifications(self, mock_mail):
        msg = notifications.send_stale_notifications()
        self.assertTrue(mock_mail.call_count == 1)
        self.assertTrue('Found' in msg)
        msg = notifications.send_stale_notifications(add_email=['abc@def.com',
                                                                'ghi@jkl.com'])
        self.assertTrue(mock_mail.call_count == 2)
        self.assertTrue('Found' in msg)
        n = Notification.objects.first()
        n.timestamp = timezone.now()
        n.save()
        notifications.send_stale_notifications()
        self.assertTrue(mock_mail.call_count == 2)

    @patch(
        'paying_for_college.disclosures.scripts.notifications'
        '.Notification.notify_school')
    def test_retry_notifications(self, mock_notify):
        # day_old = timezone.now() - datetime.timedelta(days=1)
        mock_notify.return_value = 'notified'
        n = Notification.objects.first()
        n.timestamp = timezone.now()
        n.save()
        msg = notifications.retry_notifications()
        self.assertTrue(mock_notify.call_count == 1)
        n.timestamp = n.timestamp - datetime.timedelta(days=4)
        n.save()
        msg = notifications.retry_notifications()
        self.assertTrue('found' in msg)

    @patch(
        'paying_for_college.disclosures.scripts.'
        'notification_tester.requests.post')
    def test_edmc_ping(self, mock_post):
        mock_return = mock.Mock()
        mock_return.ok = True
        mock_return.reason = 'OK'
        mock_return.status_code = 200
        mock_return.content = 'mock content'
        mock_post.return_value = mock_return
        resp1 = send_test_notifications()
        self.assertTrue('OK' in resp1)
        self.assertEqual(mock_post.call_count, 3)
        mock_post.side_effect = requests.exceptions.ConnectTimeout
        resp2 = send_test_notifications(url='example.com')
        self.assertTrue('timed out' in resp2)
        self.assertEqual(mock_post.call_count, 4)

    def test_calculate_percent(self):
        percent = api_utils.calculate_group_percent(100, 900)
        self.assertTrue(percent == 10.0)
        percent = api_utils.calculate_group_percent(0, 0)
        self.assertTrue(percent == 0)

    @patch('paying_for_college.disclosures.scripts.api_utils.requests.get')
    def test_search_by_school_name(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_results2
        mock_requests.return_value = mock_response
        data = api_utils.search_by_school_name('mockname')
        self.assertTrue(data == self.mock_results2['results'])

    def test_build_field_string(self):
        field_string = api_utils.build_field_string()
        self.assertTrue(field_string.startswith('id'))
        self.assertEqual(
            len(field_string.split(',')),
            (len(api_utils.BASE_FIELDS) +
             len(api_utils.YEAR_FIELDS) +
             len(api_utils.PROGRAM_FIELDS))
        )

    def test_school_has_no_control_value(self):
        process_cohorts.run(single_school=100830)
        school = School.objects.get(pk=100830)
        self.assertEqual(school.cohort_ranking_by_control, {'repay_3yr': None})

    def test_get_prepped_stats(self):
        stats = nat_stats.get_prepped_stats()
        self.assertTrue(stats['completionRateMedian'] <= 1)

    def test_get_bls_stats(self):
        stats = nat_stats.get_bls_stats()
        self.assertTrue(stats['Year'] >= 2014)

    def test_get_bls_stats_failure(self):
        m = mock_open()
        m.side_effect = FileNotFoundError
        with mock.patch('builtins.open', m):
            stats = nat_stats.get_bls_stats()
            self.assertEqual(stats, {})

    def test_compile_school_programs(self):
        mock_data = {
            'latest.academics.program_percentage.agriculture': 0.200,
            'latest.academics.program_percentage.biological': 0.100
        }
        test_payload = api_utils.compile_school_programs(mock_data)
        self.assertEqual(test_payload.get('program_count'), 2)
        self.assertEqual(
            test_payload.get('most_popular'),
            [
                'Agriculture, Agriculture Operations, and Related Sciences',
                'Biological and Biomedical Sciences'
            ]
        )

    @patch(
        'paying_for_college.disclosures.scripts.api_utils.requests.get')
    def test_get_school_programs_no_results(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.json.return_value = {}
        mock_response.ok = True
        mock_requests.return_value = mock_response
        test_payload = api_utils.compile_school_programs({})
        self.assertEqual(mock_requests.call_count, 0)
        self.assertEqual(
            test_payload.get('program_count'), 0
        )
