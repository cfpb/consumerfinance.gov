import mock
from collections import OrderedDict
from unittest import TestCase
from v1.handlers.js import JSHandler


class TestJSHandler(TestCase):
    def setUp(self):
        self.page = mock.Mock()
        self.request = mock.Mock()
        self.context = {}
        self.handler = JSHandler(self.page, self.request, self.context)

    @mock.patch('v1.handlers.js.JSHandler.set_js_dict')
    def test_process_calls_set_js_dict(self, mock_set_js_dict):
        self.handler.process()
        self.assertTrue(mock_set_js_dict.called)

    @mock.patch('v1.handlers.js.JSHandler.set_js_dict')
    def test_process_sets_context_media_to_OrderedDict(self, mock_set_js_dict):
        self.handler.process()
        self.assertIn('media', self.context)
        self.assertIsInstance(self.context['media'], OrderedDict)

    @mock.patch('v1.handlers.js.util')
    def test_set_js_dict_sets_context_to_get_page_js(self, mock_util):
        self.handler.set_js_dict()
        self.assertIn('template', self.handler.js_dict)
        self.assertEqual(self.handler.page.get_page_js(), self.handler.js_dict['template'])

    @mock.patch('v1.handlers.js.util')
    def test_set_js_dict_calls_util_get_streamfields(self, mock_util):
        js_dict = self.handler.set_js_dict()
        self.assertTrue(mock_util.get_streamfields.called)

    @mock.patch('v1.handlers.js.chain')
    @mock.patch('v1.handlers.js.util')
    @mock.patch('v1.handlers.js.JSHandler.set_block_js')
    def test_set_js_dict_calls_set_block_js_on_each_block(self, mock_set_block_js, mock_util, mock_chain):
        child = mock.Mock()
        mock_chain.return_value = [child] * 5
        self.handler.set_js_dict()
        mock_set_block_js.assert_called_with(child.block)
        self.assertEqual(mock_set_block_js.call_count, 5)

    # TODO: Test recursive method JSHandler.set_block_js

    # @mock.patch('__builtin__.issubclass')
    # @mock.patch('v1.handlers.js.JSHandler.assign_js')
    # def test_set_block_js_calls_assign_js(self, mock_assign_js, mock_issubclass):
    #     mock_issubclass.return_value = False
    #     block = mock.Mock()
    #     self.handler.set_block_js(block)
    #     mock_assign_js.assert_called_with(block)

    # @mock.patch('__builtin__.issubclass')
    # @mock.patch('v1.handlers.js.JSHandler.assign_js')
    # def test_set_block_js_calls_set_block_js_for_each_child(self, mock_assign_js, mock_issubclass):
    #     import pdb; pdb.set_trace()
    #     block = mock.Mock()
    #     child_block = mock.Mock()
    #     block.child_blocks.values.return_value = [child_block] * 5
    #     copy_sbj = JSHandler.set_block_js
    #     self.handler.set_block_js = mock.Mock()
    #     copy_sbj(self.handler, block)
    #     mock_set_block_js.assert_called_with(child_block)
    #     self.assertEqual(self.handler.set_block_js.call_count, 5)

    @mock.patch('v1.handlers.js.JSHandler.is_valid')
    def test_assign_js_calls_is_valid(self, mock_is_valid):
        obj = mock.Mock()
        mock_is_valid.return_value = False
        self.handler.assign_js(obj)
        mock_is_valid.assert_called_with(obj)

    @mock.patch('v1.handlers.js.JSHandler.is_valid')
    def test_assign_js_adds_objMediajs_uniquely(self, mock_is_valid):
        obj = mock.Mock()
        obj.Media.js = ['one', 'two', 'three']
        mock_is_valid.return_value = 'atoms'
        self.handler.js_dict['atoms'] = ['one']
        self.handler.assign_js(obj)
        mock_is_valid.assert_called_with(obj)
        self.assertEqual(self.handler.js_dict['atoms'], ['one', 'two', 'three'])

    def test_is_valid_returns_False_if_object_doesnt_have_Media(self):
        obj = mock.Mock()
        result = self.handler.is_valid(obj)
        self.assertFalse(result)

    def test_is_valid_returns_False_if_objectMedia_doesnt_have_js(self):
        obj = mock.Mock()
        obj.Media = '1'
        result = self.handler.is_valid(obj)
        self.assertFalse(result)

    def test_is_valid_returns_False_if_obj_classname_not_in_JSEnum_key(self):
        obj = mock.Mock()
        obj.Media.js = ['file.js']
        obj.__class__.__name__ = 'classname'
        result = self.handler.is_valid(obj)
        self.assertFalse(result)

    @mock.patch('v1.handlers.js.JSEnum')
    def test_is_valid_returns_True_if_obj_classname_in_JSEnum_key(self, mock_enum):
        mock_enum.atoms = ['classname']
        obj = mock.Mock()
        obj.Media.js = ['file.js']
        obj.__class__.__name__ = 'classname'
        result = self.handler.is_valid(obj)
        self.assertTrue(result)
