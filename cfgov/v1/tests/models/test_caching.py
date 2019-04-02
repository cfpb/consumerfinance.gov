from django.core.files.base import ContentFile
from django.test import TestCase, override_settings

from wagtail.wagtaildocs.models import Document
from wagtail.wagtailimages.tests.utils import get_test_image_file

from core.testutils.mock_cache_backend import CACHE_PURGED_URLS
from v1.models.caching import (
    AkamaiBackend, cloudfront_cache_invalidation
)
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
        self.assertEquals(akamai_backend.client_token, 'token')
        self.assertEquals(akamai_backend.client_secret, 'secret')
        self.assertEquals(akamai_backend.access_token, 'access token')


@override_settings(WAGTAILFRONTENDCACHE={
    'varnish': {
        'BACKEND': 'core.testutils.mock_cache_backend.MockCacheBackend',
    },
})
class CloudfrontInvalidationTest(TestCase):

    def setUp(self):
        self.document = Document(title="Test document")
        self.document.file.save(
            'example.txt',
            ContentFile("A boring example document")
        )
        self.image = CFGOVImage.objects.create(
            title='test',
            file=get_test_image_file()
        )

        CACHE_PURGED_URLS[:] = []

    def tearDown(self):
        self.document.file.delete()

    @override_settings(AWS_S3_CUSTOM_DOMAIN='https://foo/')
    def test_rendition_saved_cache_invalidation_with_custom_domain(self):
        rendition = self.image.get_rendition('original')
        cloudfront_cache_invalidation(None, rendition)
        self.assertIn('https://foo' + rendition.url, CACHE_PURGED_URLS)

    def test_rendition_saved_cache_invalidation_without_custom_domain(self):
        rendition = self.image.get_rendition('original')
        cloudfront_cache_invalidation(None, rendition)
        self.assertIn(rendition.url, CACHE_PURGED_URLS)

    @override_settings(AWS_S3_CUSTOM_DOMAIN='https://foo/')
    def test_document_saved_cache_invalidation_with_custom_domain(self):
        cloudfront_cache_invalidation(None, self.document)
        self.assertIn('https://foo' + self.document.url, CACHE_PURGED_URLS)

    def test_document_saved_cache_invalidation_without_custom_domain(self):
        cloudfront_cache_invalidation(None, self.document)
        self.assertIn(self.document.url, CACHE_PURGED_URLS)
