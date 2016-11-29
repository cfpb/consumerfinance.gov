from unittest import TestCase

from sheerlike.helpers import process_string_fields


class TestProcessStringFields(TestCase):
    @staticmethod
    def double(num):
        return str(2 * int(num))

    def test_non_string_does_nothing(self):
        self.assertEqual(process_string_fields(3, callback=self.double), 3)

    def test_simple_string(self):
        self.assertEqual(process_string_fields('3', callback=self.double), '6')

    def test_simple_list(self):
        data = ['1', '1', '2', '3', '5', '8']
        self.assertEqual(
            process_string_fields(data, callback=self.double),
            ['2', '2', '4', '6', '10', '16']
        )

    def test_simple_dict(self):
        data = {
            'a': '1',
            'b': '2',
            'c': '3',
            'd': 4,
        }
        self.assertEqual(
            process_string_fields(data, callback=self.double),
            {
                'a': '2',
                'b': '4',
                'c': '6',
                'd': 4,
            }
        )

    def test_complex(self):
        data = {
            'a': '1',
            'b': ['4', 5, 6, 7],
            'c': {
                'x': ['1', 2, 3],
            }
        }
        self.assertEqual(
            process_string_fields(data, callback=self.double),
            {
                'a': '2',
                'b': ['8', 5, 6, 7],
                'c': {
                    'x': ['2', 2, 3],
                },
            }
        )
