import json
import logging
import os
import requests

from akamai.edgegrid import EdgeGridAuth
from wagtail.contrib.wagtailfrontendcache.backends import BaseBackend

logger = logging.getLogger(__name__)


class AkamaiBackend(BaseBackend):
    def __init__(self, params):
        self.client_token = params.pop('CLIENT_TOKEN')
        self.client_secret = params.pop('CLIENT_SECRET')
        self.access_token = params.pop('ACCESS_TOKEN')
        if not all((
            self.client_token,
            self.client_secret,
            self.access_token,
        )):
            raise ValueError(
                'AKAMAI_CLIENT_TOKEN, AKAMAI_CLIENT_SECRET, '
                'AKAMAI_ACCESS_TOKEN must be configured.'
            )
        self.auth = self.get_auth()
        self.headers = {'content-type': 'application/json'}

    def get_auth(self):
        return EdgeGridAuth(
            client_token=self.client_token,
            client_secret=self.client_secret,
            access_token=self.access_token
        )

    def get_payload(self, obj):
        return {
            'action': 'invalidate',
            'objects': [obj]
        }

    def purge(self, url):
        resp = requests.post(
            os.environ['AKAMAI_FAST_PURGE_URL'],
            headers=self.headers,
            data=json.dumps(self.get_payload(obj=url)),
            auth=self.auth
        )
        logger.info(
            u'Attempted to invalidate page {url}, '
            'got back response {message}'.format(
                url=url,
                message=resp.text
            )
        )
        resp.raise_for_status()

    def purge_all(self):
        payload = self.get_payload(
            obj=os.environ['AKAMAI_OBJECT_ID']
        )
        payload['type'] = 'cpcode'
        payload['domain'] = 'production'

        resp = requests.post(
            os.environ['AKAMAI_PURGE_ALL_URL'],
            headers=self.headers,
            data=json.dumps(payload),
            auth=self.auth
        )
        logger.info(
            u'Initiated site-wide Akamai flush, '
            'got back response {message}'.format(
                message=resp.text
            )
        )
        resp.raise_for_status()
