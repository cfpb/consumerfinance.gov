# -*- coding: utf-8 -*-

import unittest
import mock

import os

import json
import wordpress_view_processor

class WordpressViewProcessorTestCase(unittest.TestCase):
    """
    wordpress_view_processor grabs views from the WordPress API and
    returns them for indexing in Elasticsearch by Sheer.

    This doesn't unittest individual functions within the module. It
    tests the `documents()` function, which is what Sheer calls, and
    ensures that the output is appropriate for the input.
    """

    @mock.patch('requests.get')
    def test_views(self, mock_requests_get):
        # /api/get_posts/?post_type=view
        mock_response_view = mock.Mock()
        mock_response_view.content = open(os.path.join(os.path.dirname(__file__),
                                    'test_wordpress_view_processor_view.json')).read()
        mock_response_hero = mock.Mock()
        mock_response_hero.content = open(os.path.join(os.path.dirname(__file__),
                                    'test_wordpress_view_processor_hero.json')).read()
        mock_requests_get.side_effect = [mock_response_view, mock_response_hero,]

        name = 'views'
        url = 'http://mockmockmock/api/get_posts/?post_type=view/'

        documents = list(wordpress_view_processor.documents(name, url))
        document = documents[0]
        custom_fields = document['custom_fields']
        related_hero = custom_fields['related_hero'][0]

        # Test that the related hero got pulled in.
        hero = document['hero']

        self.assertItemsEqual(hero['related_post'],
                              hero['custom_fields']['related_post'])


