from __future__ import unicode_literals

import json
import unittest
from cStringIO import StringIO

import mock
import unicodecsv

from data_research.mortgage_utilities.s3_utils import (
    bake_csv_to_s3, bake_json_to_s3, read_in_s3_csv, read_in_s3_json
)


class S3UtilsTests(unittest.TestCase):

    def setUp(self):

        self.sample_entry = '\{"12081": \{"county": "Manatee County"\}\}'
        self.bucket = mock.Mock(
            name='files.consumerfinance.gov',
            acls={'files.consumerfinance.gov': 'mock_acl_name'})

    @mock.patch('data_research.mortgage_utilities.s3_utils.requests.get')
    def test_read_in_s3_csv(self, mock_requests):
        mock_requests.return_value.content = 'a,b,c\nd,e,f'
        reader = read_in_s3_csv('fake-s3-url.com')
        self.assertEqual(mock_requests.call_count, 1)
        self.assertEqual(reader.fieldnames, ['a', 'b', 'c'])
        self.assertEqual(sorted(reader.next().values()), ['d', 'e', 'f'])

    @mock.patch('data_research.mortgage_utilities.s3_utils.requests.get')
    def test_read_in_s3_json(self, mock_requests):
        mock_return = mock.Mock()
        mock_return.json.return_value = {'test': 'test'}
        mock_requests.return_value = mock_return
        returned_json = read_in_s3_json('fake_s3_url.com')
        self.assertEqual(mock_requests.call_count, 1)
        self.assertEqual(returned_json, {'test': 'test'})

    @mock.patch('data_research.mortgage_utilities.s3_utils.boto.connect_s3')
    def test_bake_json_to_s3(self, mock_connect):
        mock_get_bucket = mock.Mock()
        mock_connect.get_bucket.return_value = mock_get_bucket
        json_string = json.dumps({'test_json': 'test_payload'})
        slug = 'test.json'
        bake_json_to_s3(slug, json_string)
        self.assertEqual(mock_connect.call_count, 1)

    @mock.patch('data_research.mortgage_utilities.s3_utils.boto.connect_s3')
    def test_bake_csv_to_s3(self, mock_connect):
        mock_get_bucket = mock.Mock()
        mock_connect.get_bucket.return_value = mock_get_bucket
        csvfile = StringIO()
        writer = unicodecsv.writer(csvfile)
        writer.writerow(['a', 'b', 'c'])
        writer.writerow(['1', '2', '3'])
        slug = 'test.csv'
        bake_csv_to_s3(slug, csvfile)
        self.assertEqual(mock_connect.call_count, 1)
