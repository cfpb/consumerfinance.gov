from django.test import TestCase
from model_mommy import mommy

from v1.models import AbstractFilterPage, CFGOVImage, CFGOVPage


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
