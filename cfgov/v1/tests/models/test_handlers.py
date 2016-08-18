import mock
from collections import OrderedDict
from unittest import TestCase
from ...models.handlers import Handler, JSHandler


class TestHandler(TestCase):
    def setUp(self):
        self.page = mock.Mock()
        self.request = mock.Mock()
        self.handler = Handler(self.page, self.request)

    def test_process_raises_NotImplementedError(self):
        with self.assertRaises(NotImplementedError) as nie:
            self.handler.process({})

    def test_get_streamfield_blocks_returns_list(self):
        assert type(self.handler.get_streamfield_blocks()) is list


class TestJSHandler(TestCase):
    def setUp(self):
        self.page = mock.Mock()
        self.request = mock.Mock()
        self.js_handler = JSHandler(self.page, self.request)

    @mock.patch('v1.models.handlers.JSHandler.generate_js_dict')
    def test_process_calls_generate_js_dict(self, mock_generate_js_dict):
        self.js_handler.process({})
        assert mock_generate_js_dict.called

    @mock.patch('v1.models.handlers.JSHandler.generate_js_dict')
    def test_process_sets_context_media_od(self, mock_generate_js_dict):
        context = {}
        self.js_handler.process(context)
        assert 'media' in context
        assert type(context['media']) is OrderedDict

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
