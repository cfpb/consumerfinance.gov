# -*- coding: utf-8 -*-
from unittest.mock import patch

from django.test import TestCase

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
            json={
                'text': text,
                'username': username,
                'icon_url': icon
            }
        )
