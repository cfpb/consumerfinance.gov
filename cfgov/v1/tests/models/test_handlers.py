import mock
from collections import OrderedDict
from unittest import TestCase
from ...models.handlers import JSHandler


class TestJSHandler(TestCase):
    def setUp(self):
        self.page = mock.Mock()
        self.js_handler = JSHandler(self.page)

    @mock.patch('v1.models.handlers.JSHandler.generate_js_dict')
    def test_generate_js_dict_returns_OrderedDict(self, mock_generate_js_dict):
        js_handler = JSHandler(self.page)
        assert mock_generate_js_dict.called

    @mock.patch('v1.models.handlers.JSHandler.add_streamfield_js')
    def test_generate_js_dict_returns_OrderedDict(self, mock_add_sf_js):
        assert type(self.js_handler.js_dict) is OrderedDict

    @mock.patch('v1.models.handlers.JSHandler.add_streamfield_js')
    def test_generate_js_dict_calls_page_add_page_js(self, mock_add_sf_js):
        self.js_handler.generate_js_dict()
        assert self.page.add_page_js.called

    @mock.patch('v1.models.handlers.JSHandler.add_streamfield_js')
    def test_generate_js_dict_calls_add_streamfield_js(self, mock_add_sf_js):
        js_dict = self.js_handler.generate_js_dict()
        assert mock_add_sf_js.called

    def test_get_js_dict_returns_OrderedDict(self):
        self.js_handler.js_dict = OrderedDict()
        assert type(self.js_handler.get_js_dict()) is OrderedDict

    @mock.patch('v1.models.handlers.JSHandler.get_streamfield_blocks')
    @mock.patch('v1.models.handlers.JSHandler.add_block_js')
    def test_add_streamfield_js_calls_get_streamfield_blocks(self, mock_add_js, mock_get_blocks):
        self.js_handler.add_streamfield_js()
        assert mock_get_blocks.called

    @mock.patch('v1.models.handlers.JSHandler.get_streamfield_blocks')
    @mock.patch('v1.models.handlers.JSHandler.add_block_js')
    def test_add_streamfield_js_calls_add_block_js(self, mock_add_js, mock_get_blocks):
        mock_get_blocks.return_value = [mock.Mock()]
        self.js_handler.add_streamfield_js()
        assert mock_add_js.called

    @mock.patch('v1.models.handlers.JSHandler.assign_js')
    def test_add_block_js_calls_assign_js(self, mock_assign_js):
        block = mock.Mock()
        js_dict = OrderedDict()
        self.js_handler.add_block_js(block)
        assert mock_assign_js.called
        mock_assign_js.assert_called_with(block)
