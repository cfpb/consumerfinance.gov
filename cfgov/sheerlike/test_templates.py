from .templates import date_formatter


class TestTemplates(object):

    def test_date_formatter(self):
        date_string = '2012-02'
        result = date_formatter(date_string)
        assert(result == '2012-02-01')

    def test_different_date_format(self):
        date_string = '2015-02-01T22:00:00'
        date_format = '%-I:%M%p %B %-d, %Y'
        result = date_formatter(date_string, date_format)
        assert(result == '10:00PM February 1, 2015')

    def test_default_timezone_is_eastern(self):
        date_string = '2015-02-01T22:00:00'
        date_format = '%Y-%m-%d %Z'
        result = date_formatter(date_string, date_format)
        assert(result == '2015-02-01 EST')

    def test_use_different_timezone(self):
        date_string = '2015-02-01T22:00:00'
        date_format = '%Y-%m-%d %Z'
        tz = 'America/Chicago'
        result = date_formatter(date_string, date_format, tz)
        assert(result == '2015-02-01 CST')
