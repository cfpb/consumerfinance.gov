from django.core.files.base import ContentFile
from django.core.files.storage import get_storage_class
from django.test import TestCase, override_settings

from wagtail.wagtailimages import get_image_model
from wagtail.wagtailimages.tests.utils import get_test_image_file

import boto
import moto

from v1.s3utils import (
    MediaRootS3BotoStorage, http_s3_url_prefix, https_s3_url_prefix
)


@override_settings(
    AWS_QUERYSTRING_AUTH=False,
    AWS_S3_ACCESS_KEY_ID='test',
    AWS_S3_CALLING_FORMAT='boto.s3.connection.OrdinaryCallingFormat',
    AWS_S3_ROOT='root',
    AWS_S3_SECRET_ACCESS_KEY='test',
    AWS_S3_SECURE_URLS=True,
    AWS_STORAGE_BUCKET_NAME='test_s3_bucket',
    DEFAULT_FILE_STORAGE='v1.s3utils.MediaRootS3BotoStorage'
)
class S3UtilsTestCase(TestCase):
    def setUp(self):
        mock_s3 = moto.mock_s3()
        mock_s3.start()
        self.addCleanup(mock_s3.stop)

        self.s3 = boto.connect_s3()
        self.s3.create_bucket('test_s3_bucket')

    def test_s3_files_use_secure_urls(self):
        image_file = get_test_image_file(filename='test.png')

        Image = get_image_model()
        image = Image(file=image_file)

        self.assertEqual(
            image.file.url,
            'https://s3.amazonaws.com/test_s3_bucket/root/test.png'
        )

    def test_storage_location_uses_settings(self):
        storage = MediaRootS3BotoStorage()
        self.assertEqual(storage.location, 'root')

    def test_storage_writes_to_s3(self):
        f = ContentFile('content')
        Storage = get_storage_class()
        Storage().save('content.txt', f)

        bucket = self.s3.get_bucket('test_s3_bucket')
        key = bucket.get_key('root/content.txt')
        self.assertEqual(key.get_contents_as_string(), 'content')


class S3UrlPrefixTest(TestCase):
    def test_http_s3_url_prefix(self):
        with self.settings(AWS_STORAGE_BUCKET_NAME='foo.bucket'):
            self.assertEqual(
                http_s3_url_prefix(),
                'http://foo.bucket/'
            )

    def test_http_s3_url_prefix_no_setting(self):
        with self.settings(AWS_STORAGE_BUCKET_NAME=None):
            with self.assertRaises(RuntimeError):
                http_s3_url_prefix()

    def test_https_s3_url_prefix(self):
        with self.settings(AWS_STORAGE_BUCKET_NAME='foo.bucket'):
            self.assertEqual(
                https_s3_url_prefix(),
                'https://s3.amazonaws.com/foo.bucket/'
            )

    def test_https_s3_url_prefix_no_setting(self):
        with self.settings(AWS_STORAGE_BUCKET_NAME=None):
            with self.assertRaises(RuntimeError):
                https_s3_url_prefix()
