import json
import logging
import os
import requests

from akamai.edgegrid import EdgeGridAuth

from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        auth = EdgeGridAuth(
            client_token=os.environ.get('AKAMAI_CLIENT_TOKEN'),
            client_secret=os.environ.get('AKAMAI_CLIENT_SECRET'),
            access_token=os.environ.get('AKAMAI_ACCESS_TOKEN')
        )
        headers = {'content-type': 'application/json'}
        payload = {
            'action': 'invalidate',
            'type': 'cpcode',
            'domain': 'production',
            'objects': [os.environ.get('AKAMAI_OBJECT_ID')]
        }
        resp = requests.post(
            os.environ.get('AKAMAI_PURGE_ALL_URL'),
            headers=headers,
            data=json.dumps(payload),
            auth=auth
        )
        logger.info(
            'Initiated Akamai flush with response {text}'.format(
                text=resp.text
            )
        )
        resp.raise_for_status()
