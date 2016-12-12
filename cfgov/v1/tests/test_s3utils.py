import boto

from django.core.files.base import ContentFile
from django.core.files.storage import get_storage_class
from django.test import TestCase, override_settings
from moto import mock_s3

from wagtail.wagtailimages.models import get_image_model
from wagtail.wagtailimages.tests.utils import get_test_image_file


class S3UtilsTestCase(TestCase):
    @override_settings(
        AWS_QUERYSTRING_AUTH=False,
        AWS_S3_ACCESS_KEY_ID='test',
        AWS_S3_CALLING_FORMAT='boto.s3.connection.OrdinaryCallingFormat',
        AWS_S3_SECRET_ACCESS_KEY='test',
        AWS_S3_SECURE_URLS=True,
        AWS_STORAGE_BUCKET_NAME='test_s3_bucket',
        DEFAULT_FILE_STORAGE='v1.s3utils.MediaRootS3BotoStorage'
    )
    def test_s3_files_use_secure_urls(self):
        image_file = get_test_image_file(filename='test.png')

        Image = get_image_model()
        image = Image(file=image_file)

        self.assertEqual(
            image.file.url,
            'https://s3.amazonaws.com/test_s3_bucket/f/test.png'
        )

    def test_storage_location_uses_settings(self):
        with modify_settings(AWS_S3_ROOT='test'):
            from v1.s3utils import MediaRootS3BotoStorage
            storage = MediaRootS3BotoStorage()
            self.assertEqual(storage.location, 'test')


@override_settings(
    AWS_QUERYSTRING_AUTH=False,
    AWS_S3_CALLING_FORMAT='boto.s3.connection.OrdinaryCallingFormat',
    AWS_S3_ROOT='root',
    AWS_S3_SECURE_URLS=True,
    AWS_STORAGE_BUCKET_NAME='test_s3_bucket',
    DEFAULT_FILE_STORAGE='v1.s3utils.MediaRootS3BotoStorage'
)
@mock_s3
class TestS3StorageLocation(TestCase):
    def setUp(self):
        self.s3 = boto.connect_s3()
        self.s3.create_bucket('test_s3_bucket')

    def test_storage_writes_to_s3(self):
        f = ContentFile('content')
        Storage = get_storage_class()
        filename = Storage().save('content.txt', f)

        bucket = self.s3.get_bucket('test_s3_bucket')
        key = bucket.get_key('root/content.txt')
        self.assertEqual(key.get_contents_as_string(), 'content')
