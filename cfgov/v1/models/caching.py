import json
import logging
import os
from six.moves.urllib.parse import urljoin

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from wagtail.contrib.wagtailfrontendcache.backends import BaseBackend
from wagtail.contrib.wagtailfrontendcache.utils import PurgeBatch

from wagtail.wagtaildocs.models import Document
from v1.models.images import CFGOVRendition

import requests
from akamai.edgegrid import EdgeGridAuth


logger = logging.getLogger(__name__)


class AkamaiHistory(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=2083)
    message = models.CharField(max_length=255)
    user = models.ForeignKey(User)


class AkamaiBackend(BaseBackend):
    def __init__(self, params):
        self.client_token = params.get('CLIENT_TOKEN')
        self.client_secret = params.get('CLIENT_SECRET')
        self.access_token = params.get('ACCESS_TOKEN')
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
        obj = os.environ['AKAMAI_OBJECT_ID']
        resp = requests.post(
            os.environ['AKAMAI_PURGE_ALL_URL'],
            headers=self.headers,
            data=json.dumps(self.get_payload(obj=obj)),
            auth=self.auth
        )
        logger.info(
            u'Attempted to invalidate content provider {obj}, '
            'got back response {message}'.format(
                obj=obj,
                message=resp.text
            )
        )
        resp.raise_for_status()


@receiver(post_save, sender=Document)
@receiver(post_save, sender=CFGOVRendition)
def cloudfront_cache_invalidation(sender, instance, **kwargs):
    media_base = settings.MEDIA_URL
    if hasattr(settings, 'AWS_S3_CUSTOM_DOMAIN'):
        media_base = settings.AWS_S3_CUSTOM_DOMAIN

    url = urljoin(media_base, instance.url)

    logger.info("Invalidating cache for " + url)

    batch = PurgeBatch()
    batch.add_url(url)
    batch.purge(backends='cloudfront')
