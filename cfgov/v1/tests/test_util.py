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

    def test_most_common(self):
        lst = ['1', '1', '2', '3', '3', '1']
        most_common_list = util.most_common(lst)
        self.assertEquals('1', most_common_list[0])
        self.assertEquals('3', most_common_list[1])

    def test_has_active_filters_returns_True_for_search_terms_in_url(self):
        self.request.GET.items.return_value = [('key0', 'some val')]
        assert util.has_active_filters(self.request, 0)

    def test_has_active_filters_returns_False_for_nonmatching_keys_for_index(self):
        self.request.GET.items.return_value = [('key0', 'some val')]
        assert not util.has_active_filters(self.request, 1)

    def test_has_active_filters_returns_False_for_empty_values(self):
        self.request.GET.items.return_value = [('key0', '')]
        assert not util.has_active_filters(self.request, 0)
