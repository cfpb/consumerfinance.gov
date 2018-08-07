from datetime import date, datetime
from unittest import TestCase

from django.template import engines

from pytz import timezone


class DatetimesExtensionTests(TestCase):
    def setUp(self):
        self.engine = engines['wagtail-env']

    def test_date_filter(self):
        tmpl = self.engine.from_string('{{ d | date }}')
        self.assertEqual(
            tmpl.render({'d': date(2018, 2, 1)}),
            '2018-02-01'
        )

    def test_date_filter_from_string(self):
        tmpl = self.engine.from_string('{{ d | date }}')
        self.assertEqual(
            tmpl.render({'d': 'February 1st, 2018'}),
            '2018-02-01'
        )

    def test_date_filter_with_timezone(self):
        tmpl = self.engine.from_string('{{ d | date(tz=tz) }}')
        self.assertEqual(
            tmpl.render({
                'd': datetime(2018, 2, 1, 0, 0, 0,
                              tzinfo=timezone('America/New_York')),
                'tz': 'America/Chicago',
            }),
            '2018-01-31'
        )

    def test_date_formatter_default_format(self):
        tmpl = self.engine.from_string('{{ date_formatter(d) }}')
        self.assertEqual(
            tmpl.render({'d': date(2018, 2, 1)}),
            'Feb 01, 2018'
        )

    def test_date_formatter_text_format(self):
        tmpl = self.engine.from_string('{{ date_formatter(d, True) }}')
        self.assertEqual(
            tmpl.render({'d': date(2018, 2, 1)}),
            'Feb. 1, 2018'
        )

    def test_localtime(self):
        tmpl = self.engine.from_string('{{ localtime(d) }}')
        self.assertEqual(
            tmpl.render({'d': datetime(2018, 2, 1, 0, 0, 0)}),
            '2018-02-01 00:00:00'
        )

    def test_localtime_filter(self):
        tmpl = self.engine.from_string('{{ d | localtime }}')
        self.assertEqual(
            tmpl.render({'d': datetime(2018, 2, 1, 0, 0, 0)}),
            '2018-02-01 00:00:00'
        )

    def test_when_event_in_past(self):
        tmpl = self.engine.from_string('{{ when(start, end) }}')
        self.assertEqual(
            tmpl.render({
                'start': datetime(2018, 2, 1, 0, 0, 0),
                'end': datetime(2018, 2, 2, 0, 0, 0),
            }),
            'past'
        )

    def test_when_event_in_future(self):
        tmpl = self.engine.from_string('{{ when(start, end) }}')
        self.assertEqual(
            tmpl.render({
                'start': datetime(3018, 2, 1, 0, 0, 0),
                'end': datetime(3018, 2, 2, 0, 0, 0),
            }),
            'future'
        )

    def test_when_different_start_and_stream_times(self):
        tmpl = self.engine.from_string('{{ when(start, end, stream) }}')
        self.assertEqual(
            tmpl.render({
                'start': datetime(2018, 2, 1, 0, 0, 0),
                'end': datetime(3018, 2, 2, 0, 0, 0),
                'stream': datetime(3018, 2, 1, 0, 0, 0),
            }),
            'future'
        )

    def test_when_event_ongoing(self):
        tmpl = self.engine.from_string('{{ when(start, end) }}')
        self.assertEqual(
            tmpl.render({
                'start': datetime(2018, 2, 1, 0, 0, 0),
                'end': datetime(3018, 2, 1, 0, 0, 0),
            }),
            'present'
        )
