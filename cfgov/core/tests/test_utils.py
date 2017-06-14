from django.test import TestCase

from core.utils import extract_answers_from_request, slice_list


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


class TestSliceList(TestCase):
    def test_empty_list(self):
        self.assertEqual(list(slice_list([], 10)), [])

    def test_single_slice(self):
        self.assertEqual(
            list(slice_list([1, 2, 3], 1)),
            [[1, 2, 3]]
        )

    def test_equally_sized_slices(self):
        self.assertEqual(
            list(slice_list([1, 2, 3, 4, 5, 6], 3)),
            [[1, 2], [3, 4], [5, 6]]
        )

    def test_unequally_sized_slices(self):
        self.assertEqual(
            list(slice_list([1, 2, 3, 4, 5], 3)),
            [[1, 2], [3, 4], [5]]
        )
