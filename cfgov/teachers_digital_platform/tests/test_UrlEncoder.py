from django.test import TestCase

from teachers_digital_platform.UrlEncoder import UrlEncoder


_time = 1623518461


class UrlEncoderTest(TestCase):

    def setUp(self):
        self.encoder = UrlEncoder(['6-9'])

    def test_restricts_keys(self):
        with self.assertRaises(ValueError):
            UrlEncoder(['foo_bar'])

    def test_validates_key(self):
        out = self.encoder.dumps('6-9', [0, 10, 20], _time)
        self.assertIsInstance(out, str)

        with self.assertRaises(ValueError) as cm:
            self.encoder.dumps('13-20', [0, 10, 20], _time)

        self.assertEqual(cm.exception.args[0], 'key 13-20 is not valid')

    def test_stores_scores_time(self):
        dumped = self.encoder.dumps('6-9', [0, 15.25, 20], _time)
        self.assertEqual(dumped, 'v1_6-9_0:f.p:k_1uo0')

        loaded = self.encoder.loads(dumped)
        self.assertEqual(loaded['key'], '6-9')
        self.assertEqual(loaded['subtotals'], (0.0, 15.25, 20.0))
        self.assertEqual(loaded['time'], _time)

    def test_invalid_parts(self):
        bad_dump = 'v1_6-9_0:f.p:k_1uo0_bad_dump'
        loaded = self.encoder.loads(bad_dump)
        self.assertIsNone(loaded)

    def test_invalid_key(self):
        bad_dump = 'v1_13-20_0:f.p:k_1uo0'
        loaded = self.encoder.loads(bad_dump)
        self.assertIsNone(loaded)
