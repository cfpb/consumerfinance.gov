from django.test import TestCase, override_settings

from wagtail.wagtailimages.tests.utils import get_test_image_file

import boto
import moto
from model_mommy import mommy

from v1.models import AbstractFilterPage, CFGOVImage, CFGOVPage, LearnPage


class TestMetaImage(TestCase):
    def setUp(self):
        self.preview_image = mommy.prepare(CFGOVImage)
        self.social_sharing_image = mommy.prepare(CFGOVImage)

    def test_meta_image_no_images(self):
        """ Meta image should be undefined if no image provided """
        page = mommy.prepare(
            CFGOVPage,
            social_sharing_image=None
        )
        self.assertIsNone(page.meta_image)

    def test_meta_image_only_social_sharing(self):
        """ Meta image uses social sharing image if provided """
        page = mommy.prepare(
            CFGOVPage,
            social_sharing_image=self.social_sharing_image
        )
        self.assertEqual(page.meta_image, page.social_sharing_image)

    def test_meta_image_only_preview(self):
        """ AbstractFilterPages use preview image for meta image
        if a social image is not provided
        """
        page = mommy.prepare(
            AbstractFilterPage,
            social_sharing_image=None,
            preview_image=self.preview_image
        )
        self.assertEqual(page.meta_image, page.preview_image)

    def test_meta_image_both(self):
        """ AbstractFilterPages use social image for meta image
        if both preview image and social image are provided
        """
        page = mommy.prepare(
            AbstractFilterPage,
            social_sharing_image=self.social_sharing_image,
            preview_image=self.preview_image
        )
        self.assertEqual(page.meta_image, page.social_sharing_image)

    def test_template_meta_image_no_images(self):
        """Template meta tags should fallback to standard social networks."""
        page = LearnPage(social_sharing_image=None)
        response = page.serve(page.dummy_request())
        response.render()

        self.assertContains(
            response,
            (
                '<meta property="og:image" content='
                '"http://localhost/static/img/logo_open-graph_facebook.png">'
            ),
            html=True
        )

        self.assertContains(
            response,
            (
                '<meta property="twitter:image" content='
                '"http://localhost/static/img/logo_open-graph_twitter.png">'
            ),
            html=True
        )

    def check_template_meta_image_url(self, expected_root):
        """Template meta tags should use an absolute image URL."""
        image_file = get_test_image_file(filename='foo.png')
        image = mommy.make(CFGOVImage, file=image_file)
        page = LearnPage(social_sharing_image=image)
        response = page.serve(page.dummy_request())
        response.render()

        rendition_url = image.get_rendition('original').url

        self.assertContains(
            response,
            (
                '<meta property="og:image" content='
                '"{}{}">'.format(expected_root, rendition_url)
            ),
            html=True
        )

    def test_template_meta_image_url(self):
        """Meta image links should work if using local storage."""
        self.check_template_meta_image_url(expected_root="http://localhost")

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
    def test_template_image_image_url_s3(self):
        """Meta image links should work if using S3 storage."""
        mock_s3 = moto.mock_s3_deprecated()
        mock_s3.start()

        s3 = boto.connect_s3()
        s3.create_bucket('test_s3_bucket')

        try:
            # There should be no root required as the image rendition URL
            # should generate a fully qualified S3 path.
            self.check_template_meta_image_url(expected_root='')
        finally:
            mock_s3.stop()
