# -*- coding: utf-8 -*-
import json

from django.test import TestCase

from mock import patch

from alerts.mattermost_alert import MattermostAlert


class TestMattermostAlert(TestCase):

    @patch('requests.post')
    def test_post(self, mock):
        """ Test that calling MattermostAlert.post
        makes a requests post with the right parameters
        """
        webhook_url = 'www.testurl.com'
        username = 'test'
        credentials = {'username': username, 'webhook_url': webhook_url}
        text = u'foö'
        icon = 'http://some/icon.png'

        MattermostAlert(credentials, icon_url=icon).post(text)
        mock.assert_called_once_with(
            webhook_url,
            data=json.dumps({'text': text,
                             'username': username,
                             'icon_url': icon})
        )
