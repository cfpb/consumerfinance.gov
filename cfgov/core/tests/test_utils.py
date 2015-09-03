import unittest

from core.utils import extract_answers_from_request


class FakeRequest(object):
    # Quick way to simulate a request object with a POST attribute
    def __init__(self, params):
        self.POST = params


class ExtractAnswersTest(unittest.TestCase):

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
