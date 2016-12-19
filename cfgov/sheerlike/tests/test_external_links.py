from django.test import TestCase
from mock import call, patch

from sheerlike.external_links import (
    convert_http_image_links, process_external_links
)


class TestProcessExternalLinks(TestCase):
    def test_applies_parse_links(self):
        doc = {
            'foo': [
                'a',
                'b',
                ['c', 'd', 'e'],
            ],
            'bar': {
                'x': 'f',
                'y': 'g',
                'z': ['h', 'i'],
            },
        }

        with patch('sheerlike.external_links.parse_links') as parse_links:
            process_external_links(doc)
            parse_links.assert_has_calls(
                list(map(call, ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'])),
                any_order=True
            )

    def test_converts_http_link(self):
        with self.settings(AWS_STORAGE_BUCKET_NAME='bucket.name'):
            doc = '<img src="http://bucket.name/img.png"/>'
            self.assertEqual(
                process_external_links(doc),
                '<img src="https://bucket.name.s3.amazonaws.com/img.png"/>'
            )


class TestConvertHttpImageLinks(TestCase):
    def test_no_links(self):
        html = '<html><body><div>Hello</div></body></html>'
        self.assertEqual(convert_http_image_links(html), html)

    def test_no_bucket_defined(self):
        with self.settings(AWS_STORAGE_BUCKET_NAME=None):
            with self.assertRaises(RuntimeError):
                html = '<img src="http://bucket.name/img.png">'
                convert_http_image_links(html)

    def test_link_not_in_s3_bucket(self):
        with self.settings(AWS_STORAGE_BUCKET_NAME='bucket.name'):
            with self.assertRaises(ValueError):
                html = '<img src="http://other.url/img.png">'
                convert_http_image_links(html)

    def test_link_in_s3_bucket(self):
        with self.settings(AWS_STORAGE_BUCKET_NAME='bucket.name'):
            html = '<img src="http://bucket.name/img.png">'
            self.assertEqual(
                convert_http_image_links(html),
                '<img src="https://bucket.name.s3.amazonaws.com/img.png">'
            )

    def test_multiple_links(self):
        with self.settings(AWS_STORAGE_BUCKET_NAME='bucket.name'):
            html = (
                '<img src="http://bucket.name/img.png">'
                '<div>Other text</div>'
                '<img src="http://bucket.name/img2.png">'
                '<img src="/relative/img3.png">'
            )
            self.assertEqual(
                convert_http_image_links(html),
                (
                    '<img src="https://bucket.name.s3.amazonaws.com/img.png">'
                    '<div>Other text</div>'
                    '<img src="https://bucket.name.s3.amazonaws.com/img2.png">'
                    '<img src="/relative/img3.png">'
                )
            )

    def test_multiple_links_with_one_not_in_s3_bucket(self):
        with self.settings(AWS_STORAGE_BUCKET_NAME='bucket.name'):
            with self.assertRaises(ValueError):
                html = (
                    '<img src="http://bucket.name/img.png">'
                    '<img src="http://other.url/img.png">'
                )
                convert_http_image_links(html)

    def test_link_as_wordpress_image(self):
        with self.settings(AWS_STORAGE_BUCKET_NAME='bucket.name')
            html = '<img src="http://bucket.name/img.png">'
            self.assertEqual(
                convert_http_image_links(html),
                '<img src="https://bucket.name.s3.amazonaws.com/img.png">'
            )
