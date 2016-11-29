from django.test import TestCase

from processors.wordpress_cfpb_report import convert_http_image_links


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
