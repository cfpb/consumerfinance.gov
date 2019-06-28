import datetime
import os
import six

import django
from django.conf import settings
from django.utils import timezone

import requests
from paying_for_college.disclosures.scripts import (
    api_utils, nat_stats, notifications, purge_objects, tag_settlement_schools,
    update_colleges, update_ipeds
)
from paying_for_college.disclosures.scripts.ping_edmc import (
    EDMC_DEV, ERRORS, OID, notify_edmc
)
from paying_for_college.models import Alias, Notification, Program, School


if six.PY2:  # pragma: no cover
    FileNotFoundError = IOError
    import mock
    from mock import mock_open, patch
else:  # pragma: no cover
    from unittest import mock
    from unittest.mock import mock_open, patch


COLLEGE_ROOT = "{}/paying_for_college".format(settings.PROJECT_ROOT)
os.path.join(os.path.dirname(__file__), '../..')
MOCK_YAML = """\
completion_rate:\n\
  min: 0\n\
  max: 1\n\
  median: 0.4379\n\
  average_range: [.3180, .5236]\n
"""


class TaggingTests(django.test.TestCase):
    """Test functions for tagging settlement schools via CSV"""

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

    fixtures = ['test_fixture.json']

    mock_dict = {'results': [{
        'id': 155317,
        'ope6_id': 5555,
        'ope8_id': 55500,
        'enrollment': 10000,
        'accreditor': "Santa",
        'url': '',
        'degrees_predominant': '',
        'degrees_highest': '',
        'school.ownership': 2,
        'latest.completion.completion_rate_4yr_150nt_pooled': 0.45,
        'latest.completion.completion_rate_less_than_4yr_150nt_pooled': None,
        'school.main_campus': True,
        'school.online_only': False,
        'school.operating': True,
        'school.under_investigation': False,
        'RETENTRATE': '',
        'RETENTRATELT4': '',  # NEW
        'REPAY3YR': '',  # NEW
        'DEFAULTRATE': '',
        'AVGSTULOANDEBT': '',
        'MEDIANDEBTCOMPLETER': '',  # NEW
        'city': 'Lawrence'}],
        'metadata': {'page': 0}
    }

    mock_lt_4 = {'results': [{
        'id': 155317,
        'ope6_id': 5555,
        'ope8_id': 55500,
        'enrollment': 10000,
        'accreditor': "Santa",
        'url': '',
        'degrees_predominant': '',
        'degrees_highest': '',
        'school.ownership': 2,
        'latest.completion.completion_rate_4yr_150nt_pooled': 0,
        'latest.completion.completion_rate_less_than_4yr_150nt_pooled': 0.25,
        'school.main_campus': True,
        'school.online_only': False,
        'school.operating': False,
        'school.under_investigation': False,
        'RETENTRATE': '',
        'RETENTRATELT4': '',  # NEW
        'REPAY3YR': '',  # NEW
        'DEFAULTRATE': '',
        'AVGSTULOANDEBT': '',
        'MEDIANDEBTCOMPLETER': '',  # NEW
        'city': 'Lawrence'}],
        'metadata': {'page': 0}
    }
    no_data_dict = {'results': None}
    mock_dict2 = {
        'results': [{
            'id': 123456,
            'key': 'value'}],
        'metadata': {'page': 0}
    }

    def setUp(self):
        for method in ('print', 'sys.stdout'):
            base = 'paying_for_college.disclosures.scripts.update_colleges.'
            patcher = patch(base + method)
            patcher.start()
            self.addCleanup(patcher.stop)

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

    @patch(
        'paying_for_college.disclosures.scripts.update_colleges.requests.get')
    def test_update_colleges(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_dict
        mock_response.ok = True
        mock_requests.return_value = mock_response
        (FAILED, NO_DATA, endmsg) = update_colleges.update()
        self.assertTrue(len(NO_DATA) == 0)
        self.assertTrue(len(FAILED) == 0)
        self.assertTrue('updated' in endmsg)
        mock_response.json.return_value = self.no_data_dict
        (FAILED, NO_DATA, endmsg) = update_colleges.update()
        self.assertFalse(len(NO_DATA) == 0)
        mock_response.json.return_value = self.mock_lt_4
        (FAILED, NO_DATA, endmsg) = update_colleges.update()
        self.assertTrue(len(NO_DATA) == 0)

    @patch(
        'paying_for_college.disclosures.scripts.update_colleges.requests.get')
    def test_update_colleges_single_school(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_dict
        mock_response.ok = True
        mock_requests.return_value = mock_response
        (FAILED, NODATA, endmsg) = update_colleges.update(single_school=243197)
        self.assertTrue(len(NODATA) == 0)
        self.assertTrue(len(FAILED) == 0)
        self.assertTrue('updated' in endmsg)
        (FAILED, N0DATA, endmsg) = update_colleges.update(exclude_ids=[999999])
        self.assertTrue(len(NODATA) == 0)
        self.assertTrue(len(FAILED) == 0)
        self.assertTrue('updated' in endmsg)

    @patch(
        'paying_for_college.disclosures.scripts.update_colleges.requests.get')
    def test_update_colleges_not_OK(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.ok = False
        mock_response.reason = "Testing OK == False"
        mock_response.status_code = 429
        mock_requests.return_value = mock_response
        (FAILED, NO_DATA, endmsg) = update_colleges.update()
        self.assertTrue('limit' in endmsg)
        mock_response = mock.Mock()
        mock_response.ok = False
        mock_response.reason = "Testing OK == False"
        (FAILED, NO_DATA, endmsg) = update_colleges.update()
        self.assertFalse(len(FAILED) == 0)
        mock_requests.side_effect = requests.exceptions.ConnectTimeout
        (FAILED, NO_DATA, endmsg) = update_colleges.update()
        self.assertFalse(len(FAILED) == 0)

    @patch(
        'paying_for_college.disclosures.scripts.update_colleges.requests.get')
    def test_update_colleges_bad_responses(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.ok = True
        mock_response.json.return_value = {'results': []}
        (FAILED, NO_DATA, endmsg) = update_colleges.update()
        self.assertTrue('no data' in endmsg)

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
        with patch("six.moves.builtins.open", m, create=True):
            update_ipeds.dump_csv(
                '/tmp/mockfile.csv',
                ['a', 'b', 'c'],
                [{'a': 'd', 'b': 'e', 'c': 'f'}])

        self.assertTrue(m.call_count == 1)

    def test_write_clean_csv(self):
        m = mock_open()
        with patch("six.moves.builtins.open", m, create=True):
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
        with patch("six.moves.builtins.open", m):
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
        mock_dict = update_ipeds.process_datafiles()
        self.assertTrue(mock_read.call_count == 2)
        self.assertTrue('999999' in mock_dict.keys())
        mock_fieldnames = ['UNITID'] + list(school_points.keys())
        mock_return_dict = {school_points[key]: 'x' for key in school_points}
        mock_return_dict['UNITID'] = '999999'
        mock_read.return_value = (mock_fieldnames, [mock_return_dict])
        mock_dict = update_ipeds.process_datafiles(add_schools=['999999'])
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

    @patch('paying_for_college.disclosures.scripts.ping_edmc.requests.post')
    def test_edmc_ping(self, mock_post):
        mock_return = mock.Mock()
        mock_return.ok = True
        mock_return.reason = 'OK'
        mock_return.status_code = 200
        mock_post.return_value = mock_return
        resp1 = notify_edmc(EDMC_DEV, OID, ERRORS)
        self.assertTrue('OK' in resp1)
        self.assertTrue(mock_post.call_count == 1)
        mock_post.side_effect = requests.exceptions.ConnectTimeout
        resp2 = notify_edmc(EDMC_DEV, OID, ERRORS)
        self.assertTrue('timed' in resp2)
        self.assertTrue(mock_post.call_count == 2)

    def test_calculate_percent(self):
        percent = api_utils.calculate_group_percent(100, 900)
        self.assertTrue(percent == 10.0)
        percent = api_utils.calculate_group_percent(0, 0)
        self.assertTrue(percent == 0)

    @patch('paying_for_college.disclosures.scripts.api_utils.requests.get')
    def test_get_repayment_data(self, mock_requests):
        mock_response = mock.Mock()
        expected_dict = {
            'results': [
                {'latest.repayment.5_yr_repayment.completers': 100,
                 'latest.repayment.5_yr_repayment.noncompleters': 900}]
        }
        mock_response.json.return_value = expected_dict
        mock_requests.return_value = mock_response
        data = api_utils.get_repayment_data(123456)
        self.assertTrue(data['completer_repayment_rate_after_5_yrs'] == 10.0)

    @patch('paying_for_college.disclosures.scripts.api_utils.requests.get')
    def test_search_by_school_name(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_dict2
        mock_requests.return_value = mock_response
        data = api_utils.search_by_school_name('mockname')
        self.assertTrue(data == self.mock_dict2['results'])

    def test_build_field_string(self):
        fstring = api_utils.build_field_string()
        self.assertTrue(fstring.startswith('id'))
        self.assertTrue(fstring.endswith('25000'))

    @patch('paying_for_college.disclosures.scripts.nat_stats.requests.get')
    def test_bad_nat_stats_request(self, mock_requests):
        mock_requests.side_effect = requests.exceptions.ConnectionError
        self.assertEqual(nat_stats.get_stats_yaml(), {})

    @patch('paying_for_college.disclosures.scripts.nat_stats.yaml.safe_load')
    @patch('paying_for_college.disclosures.scripts.nat_stats.requests.get')
    def test_nat_stats_request_returns_none(self, mock_requests, mock_yaml):
        mock_yaml.side_effect = AttributeError
        self.assertEqual(nat_stats.get_stats_yaml(), {})

    @patch('paying_for_college.disclosures.scripts.nat_stats.requests.get')
    def test_get_stats_yaml(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.text = MOCK_YAML
        mock_response.ok = True
        mock_requests.return_value = mock_response
        data = nat_stats.get_stats_yaml()
        self.assertTrue(mock_requests.call_count == 1)
        self.assertTrue(data['completion_rate']['max'] == 1)
        mock_response.ok = False
        mock_requests.return_value = mock_response
        data = nat_stats.get_stats_yaml()
        self.assertTrue(mock_requests.call_count == 2)
        self.assertTrue(data == {})
        mock_requests.side_effect = requests.exceptions.ConnectTimeout
        data = nat_stats.get_stats_yaml()
        self.assertTrue(data == {})

    @patch('paying_for_college.disclosures.scripts.nat_stats.get_stats_yaml')
    def test_update_national_stats_file(self, mock_get_yaml):
        mock_get_yaml.return_value = {}
        update_try = nat_stats.update_national_stats_file()
        self.assertTrue('Could not' in update_try)

    @patch(
        'paying_for_college.disclosures.scripts.nat_stats'
        '.update_national_stats_file')
    def test_get_national_stats(self, mock_update):
        mock_update.return_value = 'OK'
        data = nat_stats.get_national_stats()
        self.assertTrue(mock_update.call_count == 0)
        self.assertTrue(data['completion_rate']['max'] == 1)
        data2 = nat_stats.get_national_stats(update=True)
        self.assertTrue(mock_update.call_count == 1)
        self.assertTrue(data2['completion_rate']['max'] == 1)
        mock_update.return_value = 'Could not'
        data = nat_stats.get_national_stats(update=True)
        self.assertTrue("retention_rate_4" in data)

    def test_get_prepped_stats(self):
        stats = nat_stats.get_prepped_stats()
        self.assertTrue(stats['completionRateMedian'] <= 1)

    def test_get_bls_stats(self):
        stats = nat_stats.get_bls_stats()
        self.assertTrue(stats['Year'] >= 2014)

    def test_get_bls_stats_failure(self):
        m = mock_open()
        m.side_effect = FileNotFoundError
        with mock.patch('six.moves.builtins.open', m):
            stats = nat_stats.get_bls_stats()
            self.assertEqual(stats, {})
