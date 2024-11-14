from django.test import SimpleTestCase

from bs4 import BeautifulSoup

from core.templatetags.svg_icon import svg_icon
from core.utils import (
    ASK_CFPB_LINKS,
    NON_CFPB_LINKS,
    add_link_markup,
    extract_answers_from_request,
    format_file_size,
    get_body_html,
    get_link_tags,
)


class FakeRequest:
    # Quick way to simulate a request object with a POST attribute
    def __init__(self, params):
        self.POST = params


class ExtractAnswersTest(SimpleTestCase):
    def test_no_answers_to_extract(self):
        request = FakeRequest({"unrelated_key": "unrelated_value"})
        result = extract_answers_from_request(request)
        assert result == []

    def test_multiple_answers_to_extract(self):
        request = FakeRequest(
            {
                "unrelated_key": "unrelated_value",
                "questionid_first": "some_answer",
                "questionid_another": "another_answer",
            }
        )
        result = extract_answers_from_request(request)
        assert result == [
            ("another", "another_answer"),
            ("first", "some_answer"),
        ]


class FormatFileSizeTests(SimpleTestCase):
    def test_format_file_size_bytes(self):
        self.assertEqual(format_file_size(124), "124 B")

    def test_format_file_size_one_kilobyte(self):
        self.assertEqual(format_file_size(1024), "1 KB")

    def test_format_file_size_kilobytes(self):
        self.assertEqual(format_file_size(1024 * 900), "900 KB")

    def test_format_file_size_megabytes(self):
        self.assertEqual(format_file_size(1024 * 9000), "9 MB")

    def test_format_file_size_gigabytes(self):
        self.assertEqual(format_file_size(1024 * 9000000), "9 GB")

    def test_format_file_size_terabytes(self):
        self.assertEqual(format_file_size(1024 * 9000000000), "8 TB")


class LinkUtilsTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.external_link_icon = svg_icon("external-link")

    def test_get_body_html_simple(self):
        self.assertEqual(
            get_body_html("outer <body>inner</body>"), "<body>inner</body>"
        )

    def test_get_body_html_full(self):
        self.assertEqual(
            get_body_html(
                "<html><head>outer</head>"
                "<body><span>inner</span></body>"
                "</html>"
            ),
            "<body><span>inner</span></body>",
        )

    def test_get_body_html_with_attributes(self):
        self.assertEqual(
            get_body_html('outer <body class="test">inner</body>'),
            '<body class="test">inner</body>',
        )

    def test_get_body_html_empty(self):
        self.assertEqual(get_body_html("outer <body></body>"), None)

    def test_get_link_tags(self):
        self.assertEqual(
            get_link_tags('outer <a href="">inner</a>'),
            [
                '<a href="">inner</a>',
            ],
        )

    def test_get_link_tags_does_not_match_aside(self):
        self.assertEqual(
            get_link_tags('outer <aside>inner <a href="">link</a></aside>'),
            [
                '<a href="">link</a>',
            ],
        )

    def test_get_link_tags_spacing(self):
        """Test for case where tag renders with only whitespace after tag name

        Template conditions within a tag, e.g.,
        `<a {% if some_condition %}class="some-class"{% endif %}>`
        can result in output with only whitespace following the tag name
        if the condition is false, like: `<a >`.
        """
        self.assertEqual(
            get_link_tags("outer <a  >inner</a>"),
            [
                "<a  >inner</a>",
            ],
        )

    def test_add_link_markup_invalid(self):
        tag = "not a valid tag"
        path = "/about-us/blog/"
        self.assertIsNone(add_link_markup(tag, path))

    def test_add_link_markup_anchor(self):
        tag = '<a href="/about-us/blog/#anchor">bar</a>'
        path = "/about-us/blog/"
        self.assertEqual(
            add_link_markup(tag, path), '<a class="" href="#anchor">bar</a>'
        )

    def check_external_link(self, url, expected_pretty_href=None):
        tag = f'<a href="{url}">foo</a>'
        path = "/about-us/blog/"
        data_pretty_href = ""

        expected_pretty_href = expected_pretty_href or url

        # Only Ask CFPB links get the data-pretty-href attribute
        if ASK_CFPB_LINKS.match(url):
            data_pretty_href = f'data-pretty-href="{expected_pretty_href}" '

        expected_html = (
            '<a class="a-link" '
            f"{data_pretty_href}"
            f'href="{url}">'
            '<span class="a-link__text">foo</span> '
            f"{self.external_link_icon}"
            "</a>"
        )
        expected_tag = BeautifulSoup(expected_html, "html.parser")

        self.assertEqual(add_link_markup(tag, path), str(expected_tag))

    def test_govdelivery_url1(self):
        url = "https://public.govdelivery.com"
        self.check_external_link(url)

    def test_govdelivery_url2(self):
        url = "https://www.govdelivery.com"
        self.check_external_link(url)

    def test_govdelivery_url3(self):
        url = "https://public.govdelivery.com/something"
        self.check_external_link(url)

    def test_dot_gov_urls(self):
        url = "https://www.federalreserve.gov"
        self.check_external_link(url, expected_pretty_href=None)

    def test_dot_gov_urls2(self):
        url = "https://www.federalreserve.gov/something"
        self.check_external_link(url, expected_pretty_href=None)

    def test_content_cfgov(self):
        url = "http://content.cfpb.gov"
        tag = f"<a href='{url}'>foo</a>"
        path = "/"
        self.assertIsNone(add_link_markup(tag, path))

    def test_urls_with_gov_in_them(self):
        url = "https://www.realgovsite.lol"
        self.check_external_link(url)

    def test_external_links_get_signed_and_icon_added(self):
        url = "https://example.com"
        self.check_external_link(url)

    def test_external_download_still_uses_external_link_icon(self):
        url = "https://example.com/file.pdf"
        self.check_external_link(url)

    def test_external_link_if_link_already_includes_left_icon(self):
        url = "https://example.com"
        tag = (
            f'<a class="a-link" href="{url}">'
            "<svg></svg>"
            '<span class="a-link__text">foo</span>'
            "</a>"
        )
        path = "/about-us/blog/"

        expected_html = (
            '<a class="a-link" '
            f'href="{url}">'
            "<svg></svg>"
            '<span class="a-link__text">foo</span> '
            f"{self.external_link_icon}"
            "</a>"
        )

        expected_tag = BeautifulSoup(expected_html, "html.parser")
        self.assertEqual(add_link_markup(tag, path), str(expected_tag))

    def test_ask_short_url(self):
        # Valid Ask CFPB URLs
        urls = [
            "/ask-cfpb/what-is-a-construction-loan-en-108/",
            "https://cfpb.gov/ask-cfpb/what-is-a-construction-loan-en-108/",
            "https://consumerfinance.gov/ask-cfpb/what-is-a-construction-loan-en-108/",  # noqa: E501
            "https://www.consumerfinance.gov/ask-cfpb/what-is-a-construction-loan-en-108/",  # noqa: E501
        ]
        path = "/"
        for url in urls:
            tag = f"<a href='{url}'>foo</a>"
            self.assertIn(
                'data-pretty-href="cfpb.gov/askcfpb/108"',
                add_link_markup(tag, path),
            )

        # Invalid Ask CFPB URLs
        urls = [
            "/ask-cfpb/not-a-valid-link/",
            "/askcfpb/123",
            "https://consumerfinance.gov/ask-cfpb-in-the-url",
            "https://consumerfinance.gov/ask-cfpb-in-the-url/123",
        ]
        for url in urls:
            tag = f"<a href='{url}'>foo</a>"
            self.assertIsNone(add_link_markup(tag, path))

    def test_link_button(self):
        url = "https://example.com"
        tag = f'<a class="a-btn" href="{url}">Click</a>'
        path = "/about-us/blog/"

        expected_html = (
            '<a class="a-btn" '
            f'href="{url}">'
            "<span>Click</span>"
            f"{self.external_link_icon}"
            "</a>"
        )

        expected_tag = BeautifulSoup(expected_html, "html.parser")

        self.assertEqual(add_link_markup(tag, path), str(expected_tag))

    def test_link_with_whitespace_in_text(self):
        url = "https://example.com"
        tag = f'<a href="{url}">\nClick <strong>here</strong> now! </a>'
        path = "/about-us/blog/"

        expected_html = (
            f'<a class="a-link" href="{url}">'
            '<span class="a-link__text">'
            "Click <strong>here</strong> now!</span> "
            f"{self.external_link_icon}"
            "</a>"
        )

        expected_tag = BeautifulSoup(expected_html, "html.parser")
        self.assertEqual(add_link_markup(tag, path), str(expected_tag))

    def test_non_cfpb_links(self):
        cfpb_urls = [
            "http://consumerfinance.gov",
            "https://consumerfinance.gov",
            "http://cfpb.gov",
            "https://cfpb.gov",
            "http://www.consumerfinance.gov",
            "https://www.consumerfinance.gov",
            "http://localhost",
            "https://localhost",
            "http://localhost:8000",
            "http://content.localhost:8000",
            "https://www.consumerfinance.gov/foo/bar/",
        ]

        for url in cfpb_urls:
            with self.subTest(url=url):
                self.assertFalse(NON_CFPB_LINKS.match(url))

        non_cfpb_urls = [
            "https://example.com/page/",
            "https://example.com/foo/www.consumerfinance.gov/bar/",
            "http://example.com/foo/cfpb.gov/bar/",
            "https://subdomain.example.com:1234",
            "https://subdomain.example.com:1234/foo/",
            "http://notconsumerfinance.gov",
        ]

        for url in non_cfpb_urls:
            with self.subTest(url=url):
                self.assertTrue(NON_CFPB_LINKS.match(url))
