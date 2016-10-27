from django.test import TestCase
from wagtail.wagtailimages.models import get_image_model
from wagtail.wagtailimages.tests.utils import get_test_image_file


class S3UtilsTestCase(TestCase):
    def test_s3_files_use_secure_urls(self):
        test_bucket = 'bucket.test'
        filename = 'test.png'

        image_file = get_test_image_file(filename=filename)

        Image = get_image_model()
        image = Image(file=image_file)

        with self.settings(
            AWS_QUERYSTRING_AUTH=False,
            AWS_S3_ACCESS_KEY_ID='test',
            AWS_S3_SECRET_ACCESS_KEY='test',
            AWS_S3_SECURE_URLS=True,
            AWS_STORAGE_BUCKET_NAME=test_bucket,
            DEFAULT_FILE_STORAGE='v1.s3utils.MediaRootS3BotoStorage',
        ):
            expected_url = 'https://{}.s3.amazonaws.com/f/{}'.format(
                test_bucket,
                filename
            )

            self.assertEqual(image.file.url, expected_url)
