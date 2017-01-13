import json

import mock
from django.test import TestCase

from v1.models import CFGOVPage
from v1.tests.wagtail_pages import helpers

from ..util import util


class TestUtilFunctions(TestCase):

    def setUp(self):
        self.page = mock.Mock()
        self.request = mock.Mock()

        self.new_page = CFGOVPage(title='a cfgov page')
        self.new_page.live = False
        self.new_page.shared = False

        helpers.save_new_page(self.new_page)

    @mock.patch('__builtin__.isinstance')
    @mock.patch('__builtin__.vars')
    @mock.patch('v1.util.util.StreamValue')
    def get_streamfields_returns_dict_of_streamfields(
            self, mock_streamvalueclass, mock_vars, mock_isinstance):
        page = mock.Mock()
        mock_vars.items.return_value = {'key': 'value'}
        mock_isinstance.return_value = True
        result = util.get_streamfields(page)
        self.assertEqual(result, {'key': 'value'})
