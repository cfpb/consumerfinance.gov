from django.core.files.base import ContentFile
from django.core.files.storage import get_storage_class
from django.test import TestCase, override_settings

from wagtail.wagtailimages import get_image_model
from wagtail.wagtailimages.tests.utils import get_test_image_file

import boto3
import moto

from v1.s3utils import http_s3_url_prefix, https_s3_url_prefix


@override_settings(
    AWS_LOCATION='root',
    AWS_S3_ACCESS_KEY_ID='test',
    AWS_S3_SECRET_ACCESS_KEY='test',
    AWS_STORAGE_BUCKET_NAME='test_s3_bucket',
    DEFAULT_FILE_STORAGE='storages.backends.s3boto3.S3Boto3Storage'
)
class S3UtilsTestCase(TestCase):
    def setUp(self):
        mock_s3 = moto.mock_s3()
        mock_s3.start()
        self.addCleanup(mock_s3.stop)

        self.s3 = boto3.client('s3')
        self.s3.create_bucket(Bucket='test_s3_bucket')

    def test_s3_files_use_secure_urls(self):
        image_file = get_test_image_file(filename='test.png')

        Image = get_image_model()
        image = Image(file=image_file)

        self.assertEqual(
            image.file.url,
            'https://s3.amazonaws.com/test_s3_bucket/root/test.png'
        )

    def test_storage_writes_to_s3(self):
        f = ContentFile('test content')
        Storage = get_storage_class()
        Storage().save('content.txt', f)

        response = self.s3.get_object(
            Bucket='test_s3_bucket',
            Key='root/content.txt'
        )
        self.assertEqual(response['Body'].read(), 'test content')


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
