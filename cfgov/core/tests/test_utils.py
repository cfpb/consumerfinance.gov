import re
import unittest

from django.test import TestCase

from core.utils import (
    add_link_markup, extract_answers_from_request, format_file_size,
    get_body_html, get_link_tags
)


VALID_LINK_MARKUP = re.compile(
r'<a class="a-link a-link__icon" '  # noqa: E122
   r'data-pretty-href="https://example.com(/[\w\.]+)?" '  # noqa: E121
   r'href="/external-site/\?ext_url=https%3A%2F%2Fexample.com(%2F[\w\.]+)?&amp;signature=\w+">'  # noqa: E501
    r'<span class="a-link_text">foo</span> '  # noqa: E131
    r'<svg class="cf-icon-svg".*>.+</svg>'  # noqa: E501
r'\n?</a>'  # noqa: E122
)


class FakeRequest(object):
    # Quick way to simulate a request object with a POST attribute
    def __init__(self, params):
        self.POST = params


class ExtractAnswersTest(TestCase):

    def test_no_answers_to_extract(self):
        request = FakeRequest({'unrelated_key': 'unrelated_value'})
        result = extract_answers_from_request(request)
        assert result == []

    def test_multiple_answers_to_extract(self):
        request = FakeRequest({'unrelated_key': 'unrelated_value',
                               'questionid_first': 'some_answer',
                               'questionid_another': 'another_answer'})
        result = extract_answers_from_request(request)
        assert result == [('another', 'another_answer'),
                          ('first', 'some_answer')]


class FormatFileSizeTests(unittest.TestCase):

    def test_format_file_size_bytes(self):
        self.assertEqual(format_file_size(124), '124 B')

    def test_format_file_size_one_kilobyte(self):
        self.assertEqual(format_file_size(1024), '1 KB')

    def test_format_file_size_kilobytes(self):
        self.assertEqual(format_file_size(1024 * 900), '900 KB')

    def test_format_file_size_megabytes(self):
        self.assertEqual(format_file_size(1024 * 9000), '9 MB')

    def test_format_file_size_gigabytes(self):
        self.assertEqual(format_file_size(1024 * 9000000), '9 GB')

    def test_format_file_size_terabytes(self):
        self.assertEqual(format_file_size(1024 * 9000000000), '8 TB')


class LinkUtilsTests(TestCase):

    def test_get_body_html_simple(self):
        self.assertEqual(
            get_body_html('outer <body>inner</body>'), '<body>inner</body>'
        )

    def test_get_body_html_full(self):
        self.assertEqual(
            get_body_html(
                '<html><head>outer</head>'
                '<body><span>inner</span></body>'
                '</html>'
            ),
            '<body><span>inner</span></body>'
        )

    def test_get_body_html_with_attributes(self):
        self.assertEqual(
            get_body_html('outer <body class="test">inner</body>'),
            '<body class="test">inner</body>'
        )

    def test_get_body_html_empty(self):
        self.assertEqual(
            get_body_html('outer <body></body>'), None
        )

    def test_get_link_tags(self):
        self.assertEqual(
            get_link_tags('outer <a href="">inner</a>'),
            ['<a href="">inner</a>', ]
        )

    def test_get_link_tags_does_not_match_aside(self):
        self.assertEqual(
            get_link_tags('outer <aside>inner <a href="">link</a></aside>'),
            ['<a href="">link</a>', ]
        )

    def test_get_link_tags_spacing(self):
        """Test for case where tag renders with only whitespace after tag name

        Template conditions within a tag, e.g.,
        `<a {% if some_condition %}class="some-class"{% endif %}>`
        can result in output with only whitespace following the tag name
        if the condition is false, like: `<a >`.
        """
        self.assertEqual(
            get_link_tags('outer <a  >inner</a>'),
            ['<a  >inner</a>', ]
        )

    def test_add_link_markup_invalid(self):
        tag = 'not a valid tag'
        path = '/about-us/blog/'
        self.assertEqual(
            add_link_markup(tag, path),
            None
        )

    def test_add_link_markup_anchor(self):
        tag = '<a href="/about-us/blog/#anchor">bar</a>'
        path = '/about-us/blog/'
        self.assertEqual(
            add_link_markup(tag, path),
            '<a class="" href="#anchor">bar</a>'
        )

    def test_add_link_markup_external(self):
        tag = '<a href="/external-site/?ext_url=https%3A%2F%2Fexample.com">foo</a>'  # noqa: E501
        path = '/about-us/blog/'
        self.assertRegex(
            add_link_markup(tag, path),
            VALID_LINK_MARKUP
        )

    def test_add_link_markup_non_cfpb(self):
        tag = '<a href="https://example.com">foo</a>'
        path = '/about-us/blog/'
        self.assertRegex(
            add_link_markup(tag, path),
            VALID_LINK_MARKUP
        )

    def test_add_link_markup_download(self):
        tag = '<a href="https://example.com/file.pdf">foo</a>'
        path = '/about-us/blog/'
        self.assertRegex(
            add_link_markup(tag, path),
            VALID_LINK_MARKUP
        )

    def test_ask_short_url(self):
        # Valid Ask CFPB URLs
        urls = [
            '/ask-cfpb/what-is-a-construction-loan-en-108/',
            'https://cfpb.gov/ask-cfpb/what-is-a-construction-loan-en-108/',
            'https://consumerfinance.gov/ask-cfpb/what-is-a-construction-loan-en-108/',  # noqa: E501
            'https://www.consumerfinance.gov/ask-cfpb/what-is-a-construction-loan-en-108/'  # noqa: E501
        ]
        path = '/'
        for url in urls:
            tag = ("<a href='{}'>foo</a>".format(url))
            self.assertIn(
                'data-pretty-href="cfpb.gov/askcfpb/108"',
                add_link_markup(tag, path)
            )

        # Invalid Ask CFPB URLs
        urls = [
            '/ask-cfpb/not-a-valid-link/',
            '/askcfpb/123',
            'https://consumerfinance.gov/ask-cfpb-in-the-url',
            'https://consumerfinance.gov/ask-cfpb-in-the-url/123'
        ]
        for url in urls:
            tag = ("<a href='{}'>foo</a>".format(url))
            self.assertIsNone(add_link_markup(tag, path))
