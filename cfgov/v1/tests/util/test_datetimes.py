from datetime import date, datetime

from django.test import TestCase

from pytz import timezone

from v1.util.datetimes import convert_date, end_of_time_period


class TestDateTime(TestCase):
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

    # full_date testing both date delimiters
    def test_end_of_time_period_returns_full_date(self):
        result = end_of_time_period('4/14/2021', date(2021, 4, 14))
        self.assertEqual(result, date(2021, 4, 14))

    def test_end_of_time_period_returns_same_full_date(self):
        result = end_of_time_period('4-15-2021', date(2021, 4, 15))
        self.assertEqual(result, date(2021, 4, 15))

    # end_of_month testing both date delimiters
    def test_end_of_month_returns_jan_31(self):
        result = end_of_time_period('1/21', date(2021, 1, 1))
        self.assertEqual(result, date(2021, 1, 31))

    def test_end_of_month_returns_feb_28(self):
        result = end_of_time_period('2/2021', date(2021, 2, 1))
        self.assertEqual(result, date(2021, 2, 28))

    def test_end_of_month_returns_mar_31(self):
        result = end_of_time_period('3-21', date(2021, 3, 1))
        self.assertEqual(result, date(2021, 3, 31))

    def test_end_of_month_returns_apr_30(self):
        result = end_of_time_period('4-2020', date(2020, 4, 1))
        self.assertEqual(result, date(2020, 4, 30))

    def test_end_of_month_returns_jun_30(self):
        result = end_of_time_period('6-20', date(2020, 6, 1))
        self.assertEqual(result, date(2020, 6, 30))

    def test_end_of_month_returns_sep_30(self):
        result = end_of_time_period('9/20', date(2020, 9, 1))
        self.assertEqual(result, date(2020, 9, 30))

    def test_end_of_month_returns_nov_30(self):
        result = end_of_time_period('11/2020', date(2020, 11, 1))
        self.assertEqual(result, date(2020, 11, 30))

    def test_end_of_month_returns_dec_31(self):
        result = end_of_time_period('12-2020', date(2020, 12, 1))
        self.assertEqual(result, date(2020, 12, 31))

    def test_end_of_month_handles_leap_year_in_2000(self):
        result = end_of_time_period('2/00', date(2000, 2, 1))
        self.assertEqual(result, date(2000, 2, 29))

    def test_end_of_month_handles_leap_year_in_2012(self):
        result = end_of_time_period('2-12', date(2012, 2, 1))
        self.assertEqual(result, date(2012, 2, 29))

    def test_end_of_month_handles_leap_year_in_2016(self):
        result = end_of_time_period('2-2016', date(2016, 2, 1))
        self.assertEqual(result, date(2016, 2, 29))

    def test_end_of_month_handles_leap_year_in_2020(self):
        result = end_of_time_period('2/2020', date(2020, 2, 1))
        self.assertEqual(result, date(2020, 2, 29))

    # end_of_year
    def test_end_of_year_returns_dec_31(self):
        result = end_of_time_period('2020', date(2020, 1, 1))
        self.assertEqual(result, date(2020, 12, 31))

    def test_full_date_for_no_pattern_match(self):
        result = end_of_time_period('1.2.2020', date(2020, 1, 2))
        self.assertEqual(result, date(2020, 1, 2))
