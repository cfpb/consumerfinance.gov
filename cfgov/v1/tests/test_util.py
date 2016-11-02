import mock
import json

from django.test import TestCase
from django.test.client import RequestFactory

from ..util import util
from v1.tests.wagtail_pages import helpers
from v1.models import CFGOVPage
from wagtail.wagtailcore.models import PageRevision


class TestUtilFunctions(TestCase):

    def setUp(self):
        self.page = mock.Mock()
        self.request = mock.Mock()
        self.page_versions = [
            mock.Mock(**{'content_json': {'live': False, 'shared': False}}), # draft
            mock.Mock(**{'content_json': {'live': False, 'shared': True}}), # shared
            mock.Mock(**{'content_json': {'live': True, 'shared': False}}), # live
            mock.Mock(**{'content_json': {'live': True, 'shared': True}}), # live and shared
        ]
        self.page.revisions.all().order_by.return_value = self.page_versions

        self.new_page = CFGOVPage(title='a cfgov page')
        self.new_page.live = False
        self.new_page.shared = False

        helpers.save_new_page(self.new_page)
        content_json = json.loads(self.new_page.to_json())
        # create the various page revisions
        # revision 1
        content_json['title'] = 'revision 1'
        content_json['live'] = True
        content_json['shared'] = True
        self.revision_1 = self.new_page.revisions.create(content_json=json.dumps(content_json))

        # rev 2
        content_json['title'] = 'revision 2'
        content_json['live'] = True
        content_json['shared'] = False
        self.revision_2 = self.new_page.revisions.create(content_json=json.dumps(content_json))

        # rev 3
        content_json['title'] = 'revision 3'
        content_json['live'] = False
        content_json['shared'] = True
        self.revision_3 = self.new_page.revisions.create(content_json=json.dumps(content_json))

        # rev 4
        content_json['title'] = 'revision 4'
        content_json['live'] = False
        content_json['shared'] = False
        self.revision_4 = self.new_page.revisions.create(content_json=json.dumps(content_json))

    def test_production_returns_first_live_page(self):
        self.request.is_staging = False
        version = self.new_page.get_appropriate_page_version(self.request)
        self.assertEqual(version.title, 'revision 2')

    def test_shared_returns_first_shared_page(self):
        self.request.is_staging = True
        version = self.new_page.get_appropriate_page_version(self.request)
        self.assertEqual(version.title, 'revision 3')

    def test_shared_returns_None_for_only_draft_versions(self):
        self.revision_1.delete()
        self.revision_2.delete()
        self.revision_3.delete()

        version = self.new_page.get_appropriate_page_version(self.request)
        self.assertIsNone(version)

    def test_shared_returns_None_if_page_not_live_when_on_production(self):
        self.revision_1.delete()
        self.revision_2.delete()
        self.request.is_staging = False
        version = self.new_page.get_appropriate_page_version(self.request)
        self.assertIsNone(version)

    @mock.patch('__builtin__.isinstance')
    @mock.patch('__builtin__.vars')
    @mock.patch('v1.util.util.StreamValue')
    def get_streamfields_returns_dict_of_streamfields(self, mock_streamvalueclass, mock_vars, mock_isinstance):
        page = mock.Mock()
        mock_vars.items.return_value = {'key': 'value'}
        mock_isinstance.return_value = True
        result = util.get_streamfields(page)
        self.assertEqual(result, {'key': 'value'})
