import mock

from django.test import TestCase
from django.test.client import RequestFactory

from ..blocks import AbstractFormBlock, AnchorLink


class TestAbstractFormBlock(TestCase):
    def setUp(self):
        self.page = mock.Mock()
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.block_value = mock.Mock()
        self.block = AbstractFormBlock()

    @mock.patch('v1.blocks.AbstractFormBlock.get_handler_class')
    def test_get_result_calls_get_handler_class(self, mock_getclass):
        self.block.get_result(self.page, self.request, self.block_value, True)
        self.assertTrue(mock_getclass.called)

    @mock.patch('v1.blocks.AbstractFormBlock.get_handler_class')
    def test_get_result_instantiates_class(self, mock_getclass):
        self.block.get_result(self.page, self.request, self.block_value, True)
        mock_getclass()().process.assert_called_with(True)

    def test_get_handler_class_raises_AttributeError_for_unset_handler_meta(self):
        with self.assertRaises(AttributeError) as e:
            self.block.get_handler_class()

    @mock.patch('v1.blocks.import_string')
    def test_get_handler_class_returns_load_class_with_handler_path(self, mock_import):
        self.block.meta.handler = 'handler.dot.path'
        self.block.get_handler_class()
        mock_import.assert_called_with(self.block.meta.handler)

    def test_is_submitted_returns_False_for_wrong_method(self):
        result = self.block.is_submitted(self.request, 'name', 0)
        self.assertFalse(result)

    def test_is_submitted_returns_False_if_form_id_doesnt_match(self):
        self.request = self.factory.post('/', {'form_id': 'notamatch-0'})
        result = self.block.is_submitted(self.request, 'withthis', 0)
        self.assertFalse(result)

    def test_is_submitted_returns_True_for_matching_form_id(self):
        self.request = self.factory.post('/', {'form_id': 'form-match-0'})
        result = self.block.is_submitted(self.request, 'match', 0)
        self.assertTrue(result)


class TestAnchorLink(TestCase):
    def setUp(self):
        self.block = AnchorLink()

    def stringContainsNumbers(self, string):
        return any(char.isdigit() for char in string)

    @mock.patch('v1.blocks.AnchorLink.clean')
    def test_clean_calls_format_id(self, mock_format_id):
        self.data = {'link_id': 'test-string'}
        self.block.clean(self.data)
        self.assertTrue(mock_format_id.called)

    def test_clean_called_with_empty_data(self):
        self.data = {'link_id': ''}
        result = self.block.clean(self.data)
        prefix, suffix = result['link_id'].split('_')

        assert 'anchor_' in result['link_id']
        assert prefix == 'anchor'
        assert self.stringContainsNumbers(suffix)

    def test_clean_called_with_string(self):
        self.data = {'link_id': 'kittens playing with string'}
        result = self.block.clean(self.data)
        assert 'anchor_kittens-playing-with-string_' in result['link_id']

    def test_clean_called_with_existing_anchor(self):
        self.data = {'link_id': 'anchor_3472e83b2dd084'}
        result = self.block.clean(self.data)
        assert result['link_id'] == 'anchor_3472e83b2dd084'

    def test_clean_called_with_literally_anchor(self):
        self.data = {'link_id': 'anchor'}
        result = self.block.clean(self.data)

        assert 'anchor_' in result['link_id']
        assert self.stringContainsNumbers(result['link_id'])

        
