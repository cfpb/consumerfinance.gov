import json
from datetime import date

from django.test import TestCase
from django.test.client import RequestFactory

from wagtail.wagtailcore.models import PageRevision

import mock

from v1.models import CFGOVPage
from v1.tests.wagtail_pages import helpers
from v1.util import util


class TestUtilFunctions(TestCase):

    @mock.patch('__builtin__.isinstance')
    @mock.patch('__builtin__.vars')
    @mock.patch('v1.util.util.StreamValue')
    def get_streamfields_returns_dict_of_streamfields(self, mock_streamvalueclass, mock_vars, mock_isinstance):
        page = mock.Mock()
        mock_vars.items.return_value = {'key': 'value'}
        mock_isinstance.return_value = True
        result = util.get_streamfields(page)
        self.assertEqual(result, {'key': 'value'})


class TestExtendedStrftime(TestCase):

    def test_date_formatted_without_leading_zero_in_day(self):
        test_date=date(2018, 4, 5)
        formatted_date = util.extended_strftime(test_date, '%b %_d, %Y')
        self.assertEqual(formatted_date, 'Apr 5, 2018')

    def test_date_formatted_with_custom_month_abbreviation(self):
        test_date=date(2018, 9, 5)
        formatted_date = util.extended_strftime(test_date, '%_m %d, %Y')
        self.assertEqual(formatted_date, 'Sept. 05, 2018')

    def test_date_formatted_with_default_pattern(self):
        test_date=date(2018, 9, 5)
        formatted_date = util.extended_strftime(test_date, '%b %d, %Y')
        self.assertEqual(formatted_date, 'Sep 05, 2018')
