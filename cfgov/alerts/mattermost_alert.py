import os

import requests


class MattermostAlert(object):
    def __init__(self, credentials, icon_url=None):
        self.username = credentials.get(
            'username',
            os.environ.get('MATTERMOST_USERNAME')
        )
        self.webhook_url = credentials.get(
            'webhook_url',
            os.environ.get('MATTERMOST_WEBHOOK_URL')
        )
        self.icon_url = icon_url

    def post(self, text):
        payload = {
            'text': text,
            'username': self.username,
            'icon_url': self.icon_url
        }
        resp = requests.post(
            self.webhook_url,
            json=payload,
        )
        resp.raise_for_status()
