import mock
from django.test import TestCase

from v1.models.browse_page import BrowsePage
from v1.wagtail_hooks import (flush_akamai, form_module_handlers,
                              get_akamai_credentials,
                              should_flush)


class TestFormModuleHandlers(TestCase):
    def setUp(self):
        mock.patch('v1.wagtail_hooks.hooks.register')
        self.page = mock.Mock()
        self.request = mock.Mock()
        self.context = {}

    @mock.patch('__builtin__.hasattr')
    @mock.patch('v1.wagtail_hooks.util.get_streamfields')
    def test_sets_context(self, mock_getstreamfields, mock_hasattr):
        mock_hasattr.return_value = True
        child = mock.Mock()
        mock_getstreamfields().items.return_value = [('name', [child])]
        form_module_handlers(self.page, self.request, self.context)
        assert 'form_modules' in self.context

    @mock.patch('v1.wagtail_hooks.util.get_streamfields')
    def test_does_not_set_context(self, mock_getstreamfields):
        mock_getstreamfields().items.return_value = []
        form_module_handlers(self.page, self.request, self.context)
        assert 'form_modules' not in self.context

    @mock.patch('v1.wagtail_hooks.util.get_streamfields')
    def test_calls_get_streamfields(self, mock_getstreamfields):
        form_module_handlers(self.page, self.request, self.context)
        mock_getstreamfields.assert_called_with(self.page)

    @mock.patch('__builtin__.hasattr')
    @mock.patch('v1.wagtail_hooks.util.get_streamfields')
    def test_checks_child_block_if_set_form_context_exists(self, mock_getstreamfields, mock_hasattr):
        child = mock.Mock()
        streamfields = {'name': [child]}
        mock_getstreamfields.return_value = streamfields
        form_module_handlers(self.page, self.request, self.context)
        mock_hasattr.assert_called_with(child.block, 'get_result')

    @mock.patch('__builtin__.hasattr')
    @mock.patch('v1.wagtail_hooks.util.get_streamfields')
    def test_sets_context_fieldname_if_not_set(self, mock_getstreamfields, mock_hasattr):
        child = mock.Mock()
        streamfields = {'name': [child]}
        mock_getstreamfields.return_value = streamfields
        mock_hasattr.return_value = True
        form_module_handlers(self.page, self.request, self.context)
        assert 'name' in self.context['form_modules']
        self.assertIsInstance(self.context['form_modules']['name'], dict)

    @mock.patch('__builtin__.hasattr')
    @mock.patch('v1.wagtail_hooks.util.get_streamfields')
    def test_calls_child_block_get_result(self, mock_getstreamfields, mock_hasattr):
        child = mock.Mock()
        streamfields = {'name': [child]}
        mock_getstreamfields.return_value = streamfields
        mock_hasattr.return_value = True
        form_module_handlers(self.page, self.request, self.context)
        child.block.get_result.assert_called_with(
            self.page,
            self.request,
            child.value,
            child.block.is_submitted()
        )

    @mock.patch('__builtin__.hasattr')
    @mock.patch('v1.wagtail_hooks.util.get_streamfields')
    def test_calls_child_block_is_submitted(self, mock_getstreamfields, mock_hasattr):
        child = mock.Mock()
        streamfields = {'name': [child]}
        mock_getstreamfields.return_value = streamfields
        mock_hasattr.return_value = True
        form_module_handlers(self.page, self.request, self.context)
        child.block.is_submitted.assert_called_with(self.request, 'name', 0)


class TestFlushAkamai(TestCase):
    """ Tests the appropriate conditions under which we should be flushing Akamai.
    Not meant to test if the flush itself succeeded.
    """

    def setUp(self):
        self.page = BrowsePage(
            title='an arbitrary page',
            slug='an-arbitrary-page'
        )

    def test_should_not_flush_if_not_enabled(self):
        with self.settings(ENABLE_AKAMAI_CACHE_PURGE=None):
            assert not should_flush()

    def test_should_flush_if_enabled(self):
        with self.settings(ENABLE_AKAMAI_CACHE_PURGE=True):
            assert should_flush()

    def test_should_flush_gets_called_when_trying_to_flush(self):
        with mock.patch(
            'v1.wagtail_hooks.should_flush',
            return_value=False
        ) as should_flush:
            self.assertFalse(flush_akamai())
            should_flush.assert_called_once_with()


class TestGetAkamaiCredentials(TestCase):
    def test_no_credentials_raises(self):
        with self.settings(
            AKAMAI_OBJECT_ID=None,
            AKAMAI_USER=None,
            AKAMAI_PASSWORD=None
        ):
            self.assertRaises(ValueError, get_akamai_credentials)

    def test_some_credentials_raises(self):
        with self.settings(
            AKAMAI_OBJECT_ID='some-arbitrary-id',
            AKAMAI_USER=None,
            AKAMAI_PASSWORD=None
        ):
            self.assertRaises(ValueError, get_akamai_credentials)

    def test_all_credentials_returns(self):
        with self.settings(
            AKAMAI_OBJECT_ID='object-id',
            AKAMAI_USER='username',
            AKAMAI_PASSWORD='password'
        ):
            object_id, auth = get_akamai_credentials()
            self.assertEqual(object_id, 'object-id')
            self.assertIsInstance(auth, tuple)
            self.assertEqual(auth, ('username', 'password'))
