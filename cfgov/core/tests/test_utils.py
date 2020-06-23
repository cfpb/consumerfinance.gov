import unittest

from django.test import TestCase

from core.utils import (
    extract_answers_from_request, format_file_size, get_body_html,
    get_link_tags
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
