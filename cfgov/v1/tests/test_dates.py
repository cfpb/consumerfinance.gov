from datetime import date

from django.test import TestCase
from v1 import date_formatter

class TestDateFormatter(TestCase):

    def test_text_format_date(self):
        test_date = date(2018, 9, 5)
        output = date_formatter(test_date, text_format=True)
        self.assertIn('Sept. 5, 2018', output)
    
    def test_default_format_date(self):
        test_date = date(2018, 9, 5)
        output = date_formatter(test_date, text_format=False)
        self.assertIn('Sep 05, 2018', output)
