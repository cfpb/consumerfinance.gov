from django.core.files.base import ContentFile
from django.test import TestCase, override_settings

from wagtail.documents.models import Document
from wagtail.images.tests.utils import get_test_image_file

import boto3
import moto

from core.testutils.mock_cache_backend import CACHE_PURGED_URLS
from v1.models.caching import AkamaiBackend, cloudfront_cache_invalidation
from v1.models.images import CFGOVImage


class TestAkamaiBackend(TestCase):
    def test_no_credentials_raises(self):
        credentials = {
            'CLIENT_TOKEN': None,
            'CLIENT_SECRET': None,
            'ACCESS_TOKEN': None,
        }
        with self.assertRaises(ValueError):
            AkamaiBackend(credentials)

    def test_some_credentials_raises(self):
        credentials = {
            'CLIENT_TOKEN': 'some-arbitrary-token',
            'CLIENT_SECRET': None,
            'ACCESS_TOKEN': None,
        }
        with self.assertRaises(ValueError):
            AkamaiBackend(credentials)

    def test_all_credentials_get_set(self):
        credentials = {
            'CLIENT_TOKEN': 'token',
            'CLIENT_SECRET': 'secret',
            'ACCESS_TOKEN': 'access token',
        }
        akamai_backend = AkamaiBackend(credentials)
        self.assertEqual(akamai_backend.client_token, 'token')
        self.assertEqual(akamai_backend.client_secret, 'secret')
        self.assertEqual(akamai_backend.access_token, 'access token')


@override_settings(
    WAGTAILFRONTENDCACHE={
        'files': {
            'BACKEND': 'core.testutils.mock_cache_backend.MockCacheBackend',
        },
    },
)
class CloudfrontInvalidationTest(TestCase):

    def setUp(self):
        self.document = Document(title="Test document")
        self.document_without_file = Document(title="Document without file")
        self.document.file.save(
            'example.txt',
            ContentFile("A boring example document")
        )
        self.image = CFGOVImage.objects.create(
            title='test',
            file=get_test_image_file()
        )
        self.rendition = self.image.get_rendition('original')

        CACHE_PURGED_URLS[:] = []

    def tearDown(self):
        self.document.file.delete()

    def test_rendition_saved_cache_purge_disabled(self):
        cloudfront_cache_invalidation(None, self.rendition)
        self.assertEqual(CACHE_PURGED_URLS, [])

    def test_document_saved_cache_purge_disabled(self):
        cloudfront_cache_invalidation(None, self.document)
        self.assertEqual(CACHE_PURGED_URLS, [])

    @override_settings(ENABLE_CLOUDFRONT_CACHE_PURGE=True)
    def test_document_saved_cache_purge_without_file(self):
        cloudfront_cache_invalidation(None, self.document_without_file)
        self.assertEqual(CACHE_PURGED_URLS, [])

    @override_settings(ENABLE_CLOUDFRONT_CACHE_PURGE=True)
    def test_rendition_saved_cache_invalidation(self):
        cloudfront_cache_invalidation(None, self.rendition)
        self.assertIn(self.rendition.file.url, CACHE_PURGED_URLS)

    @override_settings(ENABLE_CLOUDFRONT_CACHE_PURGE=True)
    def test_document_saved_cache_invalidation(self):
        cloudfront_cache_invalidation(None, self.document)
        self.assertIn(self.document.file.url, CACHE_PURGED_URLS)
