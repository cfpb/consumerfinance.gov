from __future__ import unicode_literals

from unittest import TestCase

from legacy.templatetags.housing_counselor import split_string_list


class TestSplitStringList(TestCase):
    def test_single_entry(self):
        self.assertEqual(split_string_list('foo'), ['foo'])

    def test_multiple_services(self):
        self.assertEqual(split_string_list('foo, bar'), ['foo', 'bar'])

    def test_replaces_comma(self):
        self.assertEqual(
            split_string_list('foo, bar&#44; baz'),
            ['foo', 'bar, baz']
        )
