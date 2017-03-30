import json

import mock
from django.test import TestCase
from django.test.client import RequestFactory
from wagtail.wagtailcore.models import PageRevision

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
