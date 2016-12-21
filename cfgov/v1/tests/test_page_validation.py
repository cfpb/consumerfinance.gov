from django.test import TestCase, override_settings

from v1.page_validation import convert_http_image_links


@override_settings(MEDIA_URL='/media/')
class TestConvertHttpImageLinks(TestCase):
    def convert(self, html):
        return convert_http_image_links(
            html,
            convert_url_prefixes=[
                'http://bucket.name/',
                'http://www.com/wp-content/uploads/',
            ]
        )

    def test_no_links(self):
        html = '<html><body><div>Hello</div></body></html>'
        self.assertEqual(self.convert(html), html)

    def test_link_not_supported(self):
        with self.assertRaises(ValueError):
            html = '<img src="http://other.url/img.png">'
            self.convert(html)

    def test_link_in_supported_prefix(self):
        html = '<img src="http://bucket.name/img.png">'
        self.assertEqual(
            self.convert(html),
            '<img src="/media/img.png">'
        )

    def test_link_in_other_supported_prefix(self):
        html = '<img src="http://www.com/wp-content/uploads/a/b/c/foo.png">'
        self.assertEqual(
            self.convert(html),
            '<img src="/media/a/b/c/foo.png">'
        )

    def test_multiple_links(self):
        html = (
            '<img src="http://bucket.name/img.png">'
            '<div>Other text</div>'
            '<img src="http://www.com/wp-content/uploads/img2.png">'
            '<img src="/relative/img3.png">'
        )
        self.assertEqual(
            self.convert(html),
            (
                '<img src="/media/img.png">'
                '<div>Other text</div>'
                '<img src="/media/img2.png">'
                '<img src="/relative/img3.png">'
            )
        )

    def test_multiple_links_with_one_not_supported(self):
        with self.assertRaises(ValueError):
            html = (
                '<img src="http://bucket.name/img.png">'
                '<img src="http://other.url/img.png">'
            )
            self.convert(html)

    def test_url_not_in_image_tag(self):
        html = '<a href="http://bucket.name/img.png">'
        self.assertEqual(self.convert(html), html)
