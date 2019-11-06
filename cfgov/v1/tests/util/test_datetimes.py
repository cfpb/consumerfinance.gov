from datetime import datetime

from django.test import TestCase

from pytz import timezone

from v1.util.datetimes import convert_date


class TestConvertDate(TestCase):
    def test_convert_string(self):
        test_date_string = '2019-10-31'
        converted = convert_date(test_date_string, 'UTC')
        self.assertIsInstance(converted, datetime)
        self.assertEqual(converted.tzinfo, timezone('UTC'))

    def test_converting_naive_datetime_makes_it_aware(self):
        test_datetime = datetime.now()
        self.assertIsNone(test_datetime.tzinfo)
        converted = convert_date(test_datetime, 'UTC')
        self.assertEqual(converted.tzinfo, timezone('UTC'))

    def test_converting_aware_datetime_to_another_timezone(self):
        test_datetime = datetime.now(timezone('America/New_York'))
        converted = convert_date(test_datetime, 'UTC')
        self.assertEqual(converted.tzinfo, timezone('UTC'))
