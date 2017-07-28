from __future__ import unicode_literals

import copy
import json
import mock
import unittest

from data_research.mortgage_utilities.s3_utils import (
    bake_json_to_s3,
    prep_key,
    read_in_s3_csv,
    read_in_s3_json
)


class MockKey(object):

    def __init__(self, bucket=None, name=None):
        self.bucket = bucket
        self.name = 'data/mortgage-performance/fips.json'
        self.data = None

    def get_contents_as_string(self):
        return self.data

    def set_contents_from_string(self, s):
        self.data = copy.copy(s)

    def set_acl(self, acl_or_str, key_name='', headers=None,
                version_id=None):
        pass


class S3UtilsTests(unittest.TestCase):

    def setUp(self):

        self.sample_entry = '\{"12081": \{"county": "Manatee County"\}\}'
        self.bucket = mock.Mock(
            name='files.consumerfinance.gov',
            acls={'files.consumerfinance.gov': 'mock_acl_name'})

    def test_prep_key_function(self):
        mock_bucket = mock.Mock(name='files.consumerfinance.gov', keys={})
        mock_key = MockKey(
            mock_bucket, name='data/mortgage-performance/fips.json')
        test_key = prep_key(mock_key, self.sample_entry)
        self.assertEqual(test_key.get_contents_as_string(), self.sample_entry)

    @mock.patch('data_research.mortgage_utilities.s3_utils.requests.get')
    def test_read_in_s3_csv(self, mock_requests):
        mock_requests.return_value.content = 'a,b,c\nd,e,f'
        reader = read_in_s3_csv('fake-s3-url.com')
        self.assertEqual(mock_requests.call_count, 1)
        self.assertEqual(reader.fieldnames, ['a', 'b', 'c'])
        self.assertEqual(sorted(reader.next().values()), ['d', 'e', 'f'])

    @mock.patch('data_research.mortgage_utilities.s3_utils.boto.connect_s3')
    @mock.patch('data_research.mortgage_utilities.s3_utils.prep_key')
    def test_bake_json_to_s3(self, mock_prep_key, mock_connect):
        mock_get_bucket = mock.Mock()
        mock_connect.get_bucket.return_value = mock_get_bucket
        mock_connect
        json_string = json.dumps({'test_json': 'test_payload'})
        slug = 'test.json'
        bake_json_to_s3(slug, json_string)

    @mock.patch('data_research.mortgage_utilities.s3_utils.requests.get')
    def test_read_in_s3_json(self, mock_requests):
        mock_return = mock.Mock()
        mock_return.json.return_value = {'test': 'test'}
        mock_requests.return_value = mock_return
        returned_json = read_in_s3_json('fake_s3_url.com')
        self.assertEqual(mock_requests.call_count, 1)
        self.assertEqual(returned_json, {'test': 'test'})
