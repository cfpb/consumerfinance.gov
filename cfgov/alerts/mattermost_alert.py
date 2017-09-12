import json
import os
import requests


class MattermostAlert(object):
    def __init__(self, credentials):
        self.username = credentials.get(
            'username',
            os.environ.get('MATTERMOST_USERNAME')
        )
        self.webhook_url = credentials.get(
            'webhook_url',
            os.environ.get('MATTERMOST_WEBHOOK_URL')
        )

    def post(self, text):
        payload = {
            'text': text,
            'username': self.username,
        }
        requests.post(
            self.webhook_url,
            data=json.dumps(payload),
        )
