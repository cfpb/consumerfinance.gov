import mock

from django.test import TestCase
from django.test.client import RequestFactory

from ..util import util


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

    @mock.patch('json.loads')
    def test_production_returns_first_live_page(self, mock_json_loads):
        self.request.site.hostname = 'localhost'
        mock_json_loads.side_effect = [page.content_json for page in self.page_versions]
        util.get_appropriate_page_version(self.request, self.page)
        assert not self.page_versions[0].as_page_object.called
        assert not self.page_versions[1].as_page_object.called
        assert self.page_versions[2].as_page_object.called
        assert not self.page_versions[3].as_page_object.called

    @mock.patch('json.loads')
    def test_shared_returns_first_shared_page(self, mock_json_loads):
        self.request.site.hostname = 'content.localhost'
        mock_json_loads.side_effect = [page.content_json for page in self.page_versions]
        util.get_appropriate_page_version(self.request, self.page)
        assert not self.page_versions[0].as_page_object.called
        assert self.page_versions[1].as_page_object.called
        assert not self.page_versions[2].as_page_object.called
        assert not self.page_versions[3].as_page_object.called

    @mock.patch('json.loads')
    def test_shared_returns_None_for_only_draft_versions(self, mock_json_loads):
        self.page_versions = [
            mock.Mock(**{'content_json': {'live': False, 'shared': False}}),
            mock.Mock(**{'content_json': {'live': False, 'shared': False}}),
            mock.Mock(**{'content_json': {'live': False, 'shared': False}}),
            mock.Mock(**{'content_json': {'live': False, 'shared': False}}),
        ]
        mock_json_loads.side_effect = [page.content_json for page in self.page_versions]
        util.get_appropriate_page_version(self.request, self.page)
        assert not self.page_versions[0].as_page_object.called
        assert not self.page_versions[1].as_page_object.called
        assert not self.page_versions[2].as_page_object.called
        assert not self.page_versions[3].as_page_object.called


    @mock.patch('json.loads')
    def test_shared_returns_None_if_page_not_live_when_on_production(self, mock_json_loads):
        self.request.site.hostname = 'localhost'
        self.page_versions = [
            mock.Mock(**{'content_json': {'live': False, 'shared': True}}),
            mock.Mock(**{'content_json': {'live': False, 'shared': True}}),
            mock.Mock(**{'content_json': {'live': False, 'shared': True}}),
            mock.Mock(**{'content_json': {'live': False, 'shared': True}}),
        ]
        mock_json_loads.side_effect = [page.content_json for page in self.page_versions]
        util.get_appropriate_page_version(self.request, self.page)
        assert not self.page_versions[0].as_page_object.called
        assert not self.page_versions[1].as_page_object.called
        assert not self.page_versions[2].as_page_object.called
        assert not self.page_versions[3].as_page_object.called

    @mock.patch('__builtin__.isinstance')
    @mock.patch('__builtin__.vars')
    @mock.patch('v1.util.util.StreamValue')
    def get_streamfields_returns_dict_of_streamfields(self, mock_streamvalueclass, mock_vars, mock_isinstance):
        page = mock.Mock()
        mock_vars.items.return_value = {'key': 'value'}
        mock_isinstance.return_value = True
        result = util.get_streamfields(page)
        self.assertEqual(result, {'key': 'value'})
