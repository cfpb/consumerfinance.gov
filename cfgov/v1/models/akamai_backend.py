import json
import logging
import requests

from akamai.edgegrid import EdgeGridAuth
from wagtail.contrib.wagtailfrontendcache.backends import BaseBackend

logger = logging.getLogger(__name__)


class AkamaiBackend(BaseBackend):
    def __init__(self, params):
        self.client_token = params.pop('CLIENT_TOKEN')
        self.client_secret = params.pop('CLIENT_SECRET')
        self.access_token = params.pop('ACCESS_TOKEN')
        self.fast_purge_url = params.pop('FAST_PURGE_URL')
        if not all((
            self.client_token,
            self.client_secret,
            self.access_token,
            self.fast_purge_url
        )):
            raise ValueError(
                'AKAMAI_CLIENT_TOKEN, AKAMAI_CLIENT_SECRET, '
                'AKAMAI_ACCESS_TOKEN, AKAMAI_FAST_PURGE_URL '
                'must be configured.'
            )

    def purge(self, url):
        auth = EdgeGridAuth(
            client_token=self.client_token,
            client_secret=self.client_secret,
            access_token=self.access_token
        )
        headers = {'content-type': 'application/json'}
        payload = {
            'action': 'invalidate',
            'objects': [url]
        }
        resp = requests.post(
            self.fast_purge_url,
            headers=headers,
            data=json.dumps(payload),
            auth=auth
        )
        logger.info(
            u'Attempted to invalidate page {url}, '
            'got back response {message}'.format(
                url=url,
                message=resp.text
            )
        )
        resp.raise_for_status()
