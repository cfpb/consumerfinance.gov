from unittest import TestCase

from core.templatetags.jsonify import jsonify


class TestJsonify(TestCase):
    def test_none(self):
        self.assertEqual(jsonify(None), "null")

    def test_string(self):
        self.assertEqual(jsonify("foo"), '"foo"')

    def test_dict(self):
        self.assertEqual(jsonify({"foo": 123}), '{"foo": 123}')
