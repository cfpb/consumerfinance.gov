from django.test import TestCase
from model_mommy import mommy

from v1.models import AbstractFilterPage, CFGOVImage


class TestMetaImage(TestCase):
    def setUp(self):
        self.preview_image = mommy.prepare(CFGOVImage)
        self.social_sharing_image = mommy.prepare(CFGOVImage)

    def test_meta_image_no_images(self):
        page = mommy.prepare(
            AbstractFilterPage,
            social_sharing_image=None,
            preview_image=None
        )
        self.assertIsNone(page.meta_image)

    def test_meta_image_only_social_sharing(self):
        page = mommy.prepare(
            AbstractFilterPage,
            social_sharing_image=self.social_sharing_image,
            preview_image=None
        )
        self.assertEqual(page.meta_image, page.social_sharing_image)

    def test_meta_image_only_preview(self):
        page = mommy.prepare(
            AbstractFilterPage,
            social_sharing_image=None,
            preview_image=self.preview_image
        )
        self.assertEqual(page.meta_image, page.preview_image)

    def test_meta_image_both(self):
        page = mommy.prepare(
            AbstractFilterPage,
            social_sharing_image=self.social_sharing_image,
            preview_image=self.preview_image
        )
        self.assertEqual(page.meta_image, page.social_sharing_image)
