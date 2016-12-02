from django.test import TestCase, override_settings

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
