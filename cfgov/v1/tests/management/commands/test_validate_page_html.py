import os

from django.test import TestCase, override_settings
from mock import patch
from wagtail.wagtailcore.models import Site

from v1.management.commands.validate_page_html import Command


@override_settings(
    AWS_STORAGE_BUCKET_NAME='bucket.name',
    MEDIA_URL='/media/'
)
class TestCorrectHtml(TestCase):
    def correct_html(self, html):
        return Command().correct_html(html)

    def test_good_html(self):
        html = (
            '<p>Some text.</p>'
            '<a href="http://www.consumerfinance.gov">A link</a>'
        )
        self.assertEqual(html, self.correct_html(html))

    def test_https_image_link(self):
        html = '<img alt="foo" src="https://domain.com/image.png"/>'
        self.assertEqual(html, self.correct_html(html))

    def test_unknown_http_image_link(self):
        html = '<img alt="foo" src="http://domain.com/image.png"/>'
        with self.assertRaises(ValueError):
            self.correct_html(html)

    def test_known_http_image_link(self):
        html = '<img alt="foo" src="http://bucket.name/image.png"/>'
        self.assertEqual(
            self.correct_html(html),
            '<img alt="foo" src="/media/image.png"/>'
        )

    def test_wordpress_http_image_link(self):
        default_site = Site.objects.get(is_default_site=True)

        html = (
            '<img alt="foo" '
            'src="{}/wp-content/uploads/img.png"/>'
        ).format(default_site.root_url)

        self.assertEqual(
            self.correct_html(html),
            '<img alt="foo" src="/media/img.png"/>'
        )
