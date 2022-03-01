from django.test import TestCase, override_settings

from v1.page_validation import convert_http_image_links


@override_settings(MEDIA_URL="/media/")
class TestConvertHttpImageLinks(TestCase):
    def test_no_links(self):
        html = "<html><body><div>Hello</div></body></html>"
        self.assertEqual(convert_http_image_links(html, []), html)

    def test_no_mappings(self):
        html = '<img src="http://some.url/img.png">'
        with self.assertRaises(ValueError):
            convert_http_image_links(html, [])

    def test_link_not_supported(self):
        html = '<img src="http://some.url/img.png">'
        url_mappings = [("http://other.url", "https://other.url")]
        with self.assertRaises(ValueError):
            convert_http_image_links(html, url_mappings)

    def test_link_supported(self):
        html = '<img src="http://some.url/img.png">'
        url_mappings = [("http://some.url/", "https://other.url/")]
        self.assertEqual(
            convert_http_image_links(html, url_mappings),
            '<img src="https://other.url/img.png">',
        )

    def test_multiple_links(self):
        html = (
            '<img src="http://bucket.name/img.png">'
            "<div>Other text</div>"
            '<img src="http://www.com/static/uploads/img2.png">'
            '<img src="/relative/img3.png">'
        )
        url_mappings = [
            ("http://bucket.name/", "https://bucket.name/"),
            ("http://www.com/static/uploads/", "https://other.site/"),
        ]
        self.assertEqual(
            convert_http_image_links(html, url_mappings),
            (
                '<img src="https://bucket.name/img.png">'
                "<div>Other text</div>"
                '<img src="https://other.site/img2.png">'
                '<img src="/relative/img3.png">'
            ),
        )

    def test_multiple_links_with_one_not_supported(self):
        html = (
            '<img src="http://some.url/img.png">' '<img src="http://other.url/img.png">'
        )
        url_mappings = [("http://some.url/", "https://some.url/")]
        with self.assertRaises(ValueError):
            convert_http_image_links(html, url_mappings)

    def test_url_not_in_image_tag(self):
        html = '<a href="http://bucket.name/img.png">'
        self.assertEqual(convert_http_image_links(html, []), html)
