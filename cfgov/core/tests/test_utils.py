import unittest

from django.test import TestCase

from core.utils import (
    NoMigrations, extract_answers_from_request, format_file_size)


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
        assert sorted(result) == [('another', 'another_answer'),
                                  ('first', 'some_answer')]


class TestNoMigrations(TestCase):
    def setUp(self):
        self.nomigrations = NoMigrations()

    def test_contains(self):
        self.assertTrue('random-string' in self.nomigrations)

    def test_getitem(self):
        self.assertEqual(self.nomigrations['random-string'], 'nomigrations')


class FormatFileSizeTests(unittest.TestCase):

    def test_format_file_size_bytes(self):
        self.assertEqual(format_file_size(999), '999.0B')

    def test_format_file_size_kilobytes(self):
        self.assertEqual(format_file_size(9999), '9.8KB')

    def test_format_file_size_megabytes(self):
        self.assertEqual(format_file_size(9999999), '9.5MB')

    def test_format_file_size_gigabytes(self):
        self.assertEqual(format_file_size(9999999999), '9.3GB')

    def test_format_file_size_terabytes(self):
        self.assertEqual(format_file_size(9999999999999), '9.1TB')
