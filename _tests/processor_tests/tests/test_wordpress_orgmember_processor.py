# -*- coding: utf-8 -*-

import unittest
import mock

import os

import json
import wordpress_orgmember_processor

class WordpressOrgmemberProcessorTestCase(unittest.TestCase):
    """
    wordpress_orgmember_processor grabs orgmember from the WordPress API
    and returns them for indexing in Elasticsearch by Sheer.


    This doesn't unittest individual functions within the module. It
    tests the `documents()` function, which is what Sheer calls, and
    ensures that the output is appropriate for the input.
    """

    @mock.patch('requests.get')
    def test_orgmember(self, mock_requests_get):
        # /api/get_posts/?post_type=orgmember
        mock_response = mock.Mock()
        mock_response.content = open(os.path.join(os.path.dirname(__file__),
                                    'test_wordpress_orgmember_processor.json')).read()
        mock_requests_get.return_value = mock_response

        name = 'orgmember'
        url = 'http://mockmockmock/api/get_posts/?post_type=orgmember'

        documents = list(wordpress_orgmember_processor.documents(name, url))
        document = documents[0]
        custom_fields = document['custom_fields']
        titles = document['titles']

        self.assertEqual(len(titles), 2)


