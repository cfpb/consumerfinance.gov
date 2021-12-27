import json
import logging
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from wagtail.contrib.frontend_cache.backends import BaseBackend
from wagtail.contrib.frontend_cache.utils import PurgeBatch
from wagtail.documents.models import Document

import requests
from akamai.edgegrid import EdgeGridAuth

from v1.models.images import CFGOVRendition


logger = logging.getLogger(__name__)


class CDNHistory(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=2083)
    message = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class AkamaiBackend(BaseBackend):
    """ Akamai backend that performs an 'invalidate' purge """

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

    def get_payload(self, obj, action):
        return {
            'action': action,
            'objects': [obj]
        }

    def post_all(self, action):
        obj = os.environ['AKAMAI_OBJECT_ID']
        resp = requests.post(
            os.environ['AKAMAI_PURGE_ALL_URL'],
            headers=self.headers,
            data=json.dumps(self.get_payload(obj=obj, action=action)),
            auth=self.auth
        )
        logger.info(
            u'Attempted to {action} content provider {obj}, '
            'got back response {message}'.format(
                action=action,
                obj=obj,
                message=resp.text
            )
        )
        resp.raise_for_status()

    def post(self, url, action):
        resp = requests.post(
            os.environ['AKAMAI_FAST_PURGE_URL'],
            headers=self.headers,
            data=json.dumps(self.get_payload(obj=url, action=action)),
            auth=self.auth
        )
        logger.info(
            u'Attempted to {action} cache for page {url}, '
            'got back response {message}'.format(
                action=action,
                url=url,
                message=resp.text
            )
        )
        resp.raise_for_status()

    def post_tags(self, tags):
        """Request a deletion purge by cache_tags."""
        _url = os.getenv('AKAMAI_FAST_PURGE_URL')
        if not _url:
            logger.info(
                "Can't purge cache. No value set for 'AKAMAI_FAST_PURGE_URL'"
            )
            return
        url = _url.replace("url", "tag")
        resp = requests.post(
            url,
            headers=self.headers,
            data=json.dumps({"action": "invalidate", "objects": tags}),
            auth=self.auth
        )
        logger.info(
            f"Attempted to invalidate by cache_tags {', '.join(tags)}, "
            f"and got back the response {resp.text}"
        )
        resp.raise_for_status()

    def purge_cache_tags(self, tags):
        self.post_tags(tags)

    def purge(self, url):
        self.post(url, 'invalidate')

    def purge_all(self):
        self.post_all('invalidate')


class AkamaiDeletingBackend(AkamaiBackend):
    """ Akamai backend that performs a 'delete' purge

    This is a special-case backend, and should not be globally configured. """

    def purge(self, url):
        self.post(url, 'delete')

    def purge_all(self):
        raise NotImplementedError(
            "Purging all by deletion is intentionally not supported through "
            "this backend. Please use the Akamai Control Center."
        )


@receiver(post_save, sender=Document)
@receiver(post_save, sender=CFGOVRendition)
def cloudfront_cache_invalidation(sender, instance, **kwargs):
    if not settings.ENABLE_CLOUDFRONT_CACHE_PURGE:
        return

    if not instance.file:
        return

    url = instance.file.url

    logger.info('Purging {} from "files" cache'.format(url))

    batch = PurgeBatch()
    batch.add_url(url)
    batch.purge(backends=['files'])
