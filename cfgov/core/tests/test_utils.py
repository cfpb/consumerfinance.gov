from django.test import TestCase

from core.utils import NoMigrations, extract_answers_from_request


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
