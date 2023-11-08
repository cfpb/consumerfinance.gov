from datetime import date

from django.test import TestCase

from v1.util import util


class TestExtendedStrftime(TestCase):
    def test_date_formatted_without_leading_zero_in_day(self):
        test_date = date(2018, 4, 5)
        formatted_date = util.extended_strftime(test_date, "%b %_d, %Y")
        self.assertEqual(formatted_date, "Apr 5, 2018")

    def test_date_formatted_with_custom_month_abbreviation(self):
        test_date = date(2018, 9, 5)
        formatted_date = util.extended_strftime(test_date, "%_m %d, %Y")
        self.assertEqual(formatted_date, "Sept. 05, 2018")

    def test_date_formatted_with_default_pattern(self):
        test_date = date(2018, 9, 5)
        formatted_date = util.extended_strftime(test_date, "%b %d, %Y")
        self.assertEqual(formatted_date, "Sep 05, 2018")
