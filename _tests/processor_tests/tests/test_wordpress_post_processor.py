# -*- coding: utf-8 -*-

import unittest
import mock

import os

import json
import wordpress_post_processor

class WordpressPostProcessorTestCase(unittest.TestCase):
    """
    wordpress_post_processor grabs posts from the WordPress API and
    returns them for indexing in Elasticsearch by Sheer.

    It is currently used for the types:
        post
        newsroom
        watchroom

    This doesn't unittest individual functions within the module. It
    tests the `documents()` function, which is what Sheer calls, and
    ensures that the output is appropriate for the input.
    """

    @mock.patch('requests.get')
    def test_watchrooom(self, mock_requests_get):
        # /api/get_posts/?post_type=watchroom
        mock_response = mock.Mock()
        mock_response.content = open(os.path.join(os.path.dirname(__file__),
                                    'test_wordpress_post_processor_watchroom.json')).read()
        mock_requests_get.return_value = mock_response

        name = 'watchroom'
        url = 'http://mockmockmock/api/get_posts/?post_type=watchroom'

        documents = list(wordpress_post_processor.documents(name, url))
        document = documents[0]
        custom_fields = document['custom_fields']

        # Introspect the custom fields
        self.assertEqual(len(custom_fields), 10)
        self.assertEqual(len(custom_fields), len(document['links']))


