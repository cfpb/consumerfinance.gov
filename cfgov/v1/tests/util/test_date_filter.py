from datetime import date

from django.test import TestCase

from v1.util import date_filter


class TestDateFilter(TestCase):
    # end_of_time_period specs
    def test_end_of_time_period_returns_same_full_date(self):
        user_input = '4/29/2016'
        date_input = date(2016, 4, 29)
        result = date_filter.end_of_time_period(user_input, date_input)
        expected = date(2016, 4, 29)
        self.assertEqual(result, expected)

    def test_end_of_time_period_returns_end_of_month_for_month_year_input(self):
        user_input = '11/2016'
        date_input = date(2016, 11, 1)
        result = date_filter.end_of_time_period(user_input, date_input)
        expected = date(2016, 11, 30)
        self.assertEqual(result, expected)

    def test_end_of_time_period_returns_end_of_year_for_year_input(self):
        user_input = '2016'
        date_input = date(2016, 3, 2)
        result = date_filter.end_of_time_period(user_input, date_input)
        expected = date(2016, 12, 31)
        self.assertEqual(result, expected)

    # end_of_year specs
    def test_end_of_year_returns_dec_31(self):
        input_date = date(1998, 1, 1)
        expected_result = date(1998, 12, 31)
        self.assertEqual(date_filter.end_of_year(input_date), expected_result)

    def test_end_of_year_returns_dec_31_given_year(self):
        input_date = date(2017, 3, 25)
        expected_result = date(2017, 12, 31)
        self.assertEqual(date_filter.end_of_year(input_date), expected_result)

    # end_of_month specs
    def test_end_of_month_returns_31_of_long_months(self):
        input_date = date(2017, 3, 25)
        expected_result = date(2017, 3, 31)
        self.assertEqual(date_filter.end_of_month(input_date), expected_result)

    def test_end_of_month_returns_end_of_shorter_month(self):
        input_date = date(2019, 4, 25)
        expected_result = date(2019, 4, 30)
        self.assertEqual(date_filter.end_of_month(input_date), expected_result)

    def test_end_of_month_handles_leap_day(self):
        input_date = date(2000, 2, 1)
        expected_result = date(2000, 2, 29)
        self.assertEqual(date_filter.end_of_month(input_date), expected_result)

    def test_end_of_month_handles_december(self):
        input_date = date(2019, 12, 29)
        expected_result = date(2019, 12, 31)
        self.assertEqual(date_filter.end_of_month(input_date), expected_result)

    # date_from_format specs
    def test_date_from_pattern_returns_date_for_match(self):
        result = date_filter.date_from_pattern(
            '7/4/1776',
            '%m/%d/%Y')
        self.assertEqual(result, date(1776, 7, 4))

    def test_date_from_pattern_returns_None_for_no_match(self):
        result = date_filter.date_from_pattern(
            '2016-5-12',
            '%m/%d/%Y')
        self.assertIsNone(result)

    # determine_date_specificity specs
    def test_determine_date_specificity_returns_month_year_style(self):
        result = date_filter.determine_date_specificity('12/2017')
        self.assertEqual(result, 'month_year')

    def test_determine_date_specificity_returns_year_style(self):
        result = date_filter.determine_date_specificity('2017')
        self.assertEqual(result, 'year')

    def test_determine_date_specificity_returns_full_date_style(self):
        result = date_filter.determine_date_specificity('12/31/2017')
        self.assertEqual(result, 'full')

    def test_determine_date_specificity_returns_none_for_no_match(self):
        result = date_filter.determine_date_specificity('12.31.2017')
        self.assertEqual(result, None)
