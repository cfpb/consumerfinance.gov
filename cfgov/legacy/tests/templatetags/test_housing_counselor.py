from __future__ import unicode_literals

from unittest import TestCase

from legacy.templatetags.housing_counselor import split_services


class TestSplitServices(TestCase):
    def test_single_service(self):
        self.assertEqual(split_services('foo'), ['foo'])

    def test_multiple_services(self):
        self.assertEqual(split_services('foo, bar'), ['foo', 'bar'])

    def test_replaces_comma(self):
        self.assertEqual(
            split_services('foo, bar&#44; baz'),
            ['foo', 'bar, baz']
        )
