from django.templatetags.static import static
from django.test import TestCase

from wagtail.images.tests.utils import get_test_image_file

from model_bakery import baker

from v1.models import CFGOVImage, CFGOVPage, LearnPage


class TestMetaImage(TestCase):
    def setUp(self):
        self.social_sharing_image = baker.prepare(CFGOVImage)

    def test_meta_image_no_images(self):
        """Meta image should be undefined if no image provided"""
        page = baker.prepare(CFGOVPage, social_sharing_image=None)
        self.assertIsNone(page.meta_image)

    def test_meta_image_only_social_sharing(self):
        """Meta image uses social sharing image if provided"""
        page = baker.prepare(
            CFGOVPage, social_sharing_image=self.social_sharing_image
        )
        self.assertEqual(page.meta_image, page.social_sharing_image)

    def test_template_meta_image_no_images(self):
        """Template meta tags should fallback to standard social networks."""
        page = LearnPage(social_sharing_image=None)
        response = page.make_preview_request()
        response.render()
        self.assertContains(
            response,
            (
                '<meta property="og:image" content="http://localhost'
                f'{static("img/logo_open-graph_facebook.png")}">'
            ),
            html=True,
        )

        self.assertContains(
            response,
            (
                '<meta property="twitter:image" content="http://localhost'
                f'{static("img/logo_open-graph_twitter.png")}">'
            ),
            html=True,
        )

    def test_template_meta_image_url(self):
        """Template meta tags should use an absolute image URL."""
        image_file = get_test_image_file(filename="foo.png")
        image = baker.make(CFGOVImage, file=image_file)
        page = LearnPage(social_sharing_image=image)
        response = page.make_preview_request()
        response.render()

        rendition_url = image.get_rendition("original").url

        self.assertContains(
            response,
            (
                '<meta property="og:image" content='
                f'"http://localhost{rendition_url}">'
            ),
            html=True,
        )
