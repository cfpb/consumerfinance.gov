from django.core.exceptions import ValidationError
from django.test import TestCase

from model_bakery import baker

from v1.models.browse_filterable_page import BrowseFilterablePage
from v1.models.images import CFGOVImage
from v1.tests.wagtail_pages.helpers import save_new_page


class TestSocialSharingImage(TestCase):
    def setUp(self):
        self.page = BrowseFilterablePage(
            title='Browse Filterable Page',
            slug='browse-filterable-page',
        )
        save_new_page(self.page)

    def test_validation_error_thrown_if_width_height_too_large(self):
        self.page.social_sharing_image = baker.prepare(CFGOVImage, width=5000, height=5000)
        with self.assertRaisesRegex(
            ValidationError,
            'Social sharing image must be less than 4096w x 4096h'
        ):
            self.page.save()

    def test_validation_error_thrown_if_width_too_large(self):
        self.page.social_sharing_image = baker.prepare(CFGOVImage, width=4097, height=1500)
        with self.assertRaisesRegex(
            ValidationError,
            'Social sharing image must be less than 4096w x 4096h'
        ):
            self.page.save()

    def test_validation_error_thrown_if_height_too_large(self):
        self.page.social_sharing_image = baker.prepare(CFGOVImage, width=1500, height=4097)
        with self.assertRaisesRegex(
            ValidationError,
            'Social sharing image must be less than 4096w x 4096h'
        ):
            self.page.save()
