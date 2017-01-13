from django.test import TestCase

from sheerlike.templates import get_date_string


class TestTemplates(TestCase):

    def test_get_date_obj(self):
        date_string = '2012-02'
        result = get_date_string(date_string)
        self.assertEqual(result, '2012-02-01')

    def test_different_date_format(self):
        date_string = '2015-02-01T22:00:00'
        date_format = '%-I:%M%p %B %-d, %Y'
        result = get_date_string(date_string, date_format)
        self.assertEqual(result, '10:00PM February 1, 2015')

    def test_default_timezone_is_eastern(self):
        date_string = '2015-02-01T22:00:00'
        date_format = '%Y-%m-%d %Z'
        result = get_date_string(date_string, date_format)
        assert(result == '2015-02-01 EST' or result == '2015-02-01 EDT')

    def test_use_different_timezone(self):
        date_string = '2015-02-01T22:00:00'
        date_format = '%Y-%m-%d %Z'
        tz = 'America/Chicago'
        result = get_date_string(date_string, date_format, tz)
        self.assertEqual(result, '2015-02-01 CST')
