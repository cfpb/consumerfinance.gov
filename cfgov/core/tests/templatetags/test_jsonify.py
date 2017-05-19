from core.templatetags.jsonify import jsonify
from unittest import TestCase


class TestJsonify(TestCase):
    def test_none(self):
        self.assertEqual(jsonify(None), 'null')

    def test_string(self):
        self.assertEqual(jsonify('foo'), '"foo"')

    def test_dict(self):
        self.assertEqual(
            jsonify({'foo': 123, 'bar': 'abc'}),
            '{"foo": 123, "bar": "abc"}'
        )
