# -*- coding: utf-8 -*-

import unittest
import mock

import os

import json
import wordpress_event_processor

class WordpressEventProcessorTestCase(unittest.TestCase):
    """
    wordpress_event_processor grabs events from the WordPress API and
    returns them for indexing in Elasticsearch by Sheer.

    This doesn't unittest individual functions within the module. It
    tests the `documents()` function, which is what Sheer calls, and
    ensures that the output is appropriate for the input.
    """

    @mock.patch('requests.get')
    def test_event(self, mock_requests_get):
        # /api/get_posts/?post_type=event
        mock_response = mock.Mock()
        mock_response.content = open(os.path.join(os.path.dirname(__file__),
                                    'test_wordpress_event_processor.json')).read()
        mock_requests_get.return_value = mock_response

        name = 'event'
        url = 'http://mockmockmock/api/get_posts/?post_type=event'

        documents = list(wordpress_event_processor.documents(name, url))
        document = documents[0]
        custom_fields = document['custom_fields']

        # Ensure that the custom fields are present in the document
        self.assertIn('title', document)
        self.assertIn('published_date', document)
        self.assertIn('venue_name', document)
        self.assertIn('venue_address_address', document)
        self.assertIn('venue_address_suite', document)
        self.assertIn('venue_address_city', document)
        self.assertIn('venue_address_state', document)
        self.assertIn('venue_address_zip_code', document)
        self.assertIn('pre-event_image', document)
        self.assertIn('event_image', document)
        self.assertIn('event_date', document)
        self.assertIn('event_time', document)
        self.assertIn('event_intro', document)
        self.assertIn('event_desc', document)
        self.assertIn('reservation_desc', document)
        self.assertIn('reservation_contact_info', document)
        self.assertIn('agenda_beginning_time', document)
        self.assertIn('agenda_ending_time', document)
        self.assertIn('agenda_speaker', document)
        self.assertIn('agenda_desc', document)
        self.assertIn('agenda_venue_location', document)
        self.assertIn('live_event_image', document)
        self.assertIn('live_event_preview_image', document)
        self.assertIn('live_event_live_stream_available', document)
        self.assertIn('live_event_become_live_event', document)
        self.assertIn('post_event_become_post_event', document)
        self.assertIn('post_event_video_transcript', document)
        self.assertIn('post_event_speech_transcript', document)
        self.assertIn('post_event_image', document)
        self.assertIn('post_event_pre-image', document)
        self.assertIn('post_event_flickr_url', document)
        self.assertIn('post_event_youtube_url', document)


