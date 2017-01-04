import mock
import json

from django.test import TestCase
from django.test.client import RequestFactory

from v1.models.browse_page import BrowsePage
from v1.wagtail_hooks import (
    check_permissions, configure_page_revision, flush_akamai,
    form_module_handlers, get_akamai_credentials, share, share_the_page,
    should_flush
)


class TestShareThePage(TestCase):

    @mock.patch('wagtail.wagtailcore.hooks.register')
    def setUp(self, mock_register):
        self.page = mock.Mock()
        self.page.specific.id = 1234
        rf = RequestFactory()
        self.mock_request = {
            'saving': rf.post('/admin/pages/' + str(self.page.specific.id) + '/edit', {}),
            'sharing': rf.post('/admin/pages/' + str(self.page.specific.id) + '/edit', {'action-share': True}),
            'publishing': rf.post('/admin/pages/' + str(self.page.specific.id) + '/edit', {'action-publish': True}),
        }
        for key in self.mock_request.keys():
            self.mock_request[key].user = mock.Mock()

    @mock.patch('v1.wagtail_hooks.Page')
    @mock.patch('v1.wagtail_hooks.check_permissions')
    @mock.patch('v1.wagtail_hooks.share')
    @mock.patch('v1.wagtail_hooks.configure_page_revision')
    @mock.patch('v1.wagtail_hooks.flush_akamai')
    def test_save_draft(self, mock_flush_akamai, mock_configure_page_revision, mock_share, mock_check_permissions, mock_page):
        """
            Make sure 'Save Draft' request sets correct values for
            is_publishing and is_sharing.
        """
        mock_page.objects.get.return_value = self.page
        share_the_page(self.mock_request['saving'], self.page)
        mock_share.assert_called_once_with(self.page.specific, False, False)

    @mock.patch('v1.wagtail_hooks.Page')
    @mock.patch('v1.wagtail_hooks.check_permissions')
    @mock.patch('v1.wagtail_hooks.share')
    @mock.patch('v1.wagtail_hooks.configure_page_revision')
    @mock.patch('v1.wagtail_hooks.flush_akamai')
    def test_share_on_content(self, mock_flush_akamai, mock_configure_page_revision, mock_share, mock_check_permissions, mock_page):
        """
            Make sure 'Share on Content' request sets correct values for
            is_publishing and is_sharing.
        """
        mock_page.objects.get.return_value = self.page
        share_the_page(self.mock_request['sharing'], self.page)
        mock_share.assert_called_once_with(self.page.specific, True, False)

    @mock.patch('v1.wagtail_hooks.Page')
    @mock.patch('v1.wagtail_hooks.check_permissions')
    @mock.patch('v1.wagtail_hooks.share')
    @mock.patch('v1.wagtail_hooks.configure_page_revision')
    @mock.patch('v1.wagtail_hooks.flush_akamai')
    def test_publish_to_www(self, mock_flush_akamai, mock_configure_page_revision, mock_share, mock_check_permissions, mock_page):
        """
            Make sure 'Publish to WWW' request sets correct values for
            is_publishing and is_sharing.
        """
        mock_page.objects.get.return_value = self.page
        share_the_page(self.mock_request['publishing'], self.page)
        mock_share.assert_called_once_with(self.page.specific, False, True)

    @mock.patch('v1.wagtail_hooks.Page')
    @mock.patch('v1.wagtail_hooks.check_permissions')
    @mock.patch('v1.wagtail_hooks.share')
    @mock.patch('v1.wagtail_hooks.configure_page_revision')
    @mock.patch('v1.wagtail_hooks.flush_akamai')
    def test_function_calls(self, mock_flush_akamai, mock_configure_page_revision, mock_share, mock_check_permissions, mock_page):
        """
            Make sure all functions are called once.
        """
        mock_page.objects.get.return_value = self.page
        share_the_page(self.mock_request['publishing'], self.page)
        assert mock_flush_akamai.call_count == 1
        assert mock_configure_page_revision.call_count == 1
        assert mock_share.call_count == 1
        assert mock_check_permissions.call_count == 1


class TestCheckPermissions(TestCase):

    def setUp(self):
        self.parent = mock.Mock()
        self.user = mock.Mock()
        perms = mock.Mock()
        perms.can_publish.return_value = True
        self.parent.slug = 'root'
        self.parent.permissions_for_user.return_value = perms

    def test_calls_permissions_for_user(self):
        """
            Check call to parent page's permissions_for_user method.
        """
        check_permissions(self.parent, self.user, False, False)
        assert self.parent.permissions_for_user.called

    def test_does_not_call_can_publish(self):
        """
            Check can_publish is not called for parent.slug that is 'root'.
        """
        check_permissions(self.parent, self.user, False, False)
        perms = self.parent.permissions_for_user()
        assert not perms.can_publish.called

    def test_calls_can_publish(self):
        """
            Check can_publish is called when parent.slug is not 'root' and when
            is_publishing and is_sharing is True.
        """
        self.parent.slug = 'not root'
        check_permissions(self.parent, self.user, True, True)
        perms = self.parent.permissions_for_user()
        assert perms.can_publish.called


class TestShare(TestCase):

    def setUp(self):
        self.page = mock.Mock()
        self.page.shared = False

    def test_share_saves_page(self):
        """
            Check share saves page
        """
        share(self.page, False, False)
        assert self.page.save.called

    def test_save_a_draft(self):
        """
            Check saving a draft doesn't set anything to True.
        """
        share(self.page, False, False)
        assert not self.page.shared

    def test_share_on_content(self):
        """
            Check sharing on content sets shared to True but leaves live False.
        """
        share(self.page, True, False)
        assert self.page.shared

    def test_publish_on_www(self):
        """
            Check publish on www sets both live and shared to True.
        """
        share(self.page, False, True)
        assert self.page.shared


class TestConfigurePageRevision(TestCase):

    def setUp(self):
        self.page = mock.Mock()
        self.page.has_unshared_changes = True
        revision = mock.Mock()
        revision.content_json = '{"live": false, "shared": false}'
        self.page.get_latest_revision.return_value = revision
        self.page.live, self.page.shared = False, False

    def test_calls_get_latest_revision(self):
        configure_page_revision(self.page, False, False)
        assert self.page.get_latest_revision.called

    def test_calls_save(self):
        configure_page_revision(self.page, False, False)
        revision = self.page.get_latest_revision()
        assert revision.save.called

    def test_save_a_draft(self):
        configure_page_revision(self.page, False, False)
        latest = self.page.get_latest_revision()
        latest_content = json.loads(latest.content_json)
        assert not latest_content['shared']
        assert not latest_content['live']

    def test_sharing_a_page(self):
        configure_page_revision(self.page, True, False)
        latest = self.page.get_latest_revision()
        latest_content = json.loads(latest.content_json)
        assert latest_content['shared']
        assert not latest_content['live']

    def test_publishing_a_page(self):
        configure_page_revision(self.page, False, True)
        latest = self.page.get_latest_revision()
        latest_content = json.loads(latest.content_json)
        assert latest_content['shared']
        assert latest_content['live']


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
            assert not should_flush(self.page)

    def test_should_flush_if_enabled(self):
        with self.settings(ENABLE_AKAMAI_CACHE_PURGE=True):
            assert should_flush(self.page)

    def test_should_flush_gets_called_when_trying_to_flush(self):
        with mock.patch(
            'v1.wagtail_hooks.should_flush',
            return_value=False
        ) as should_flush:
            self.assertFalse(flush_akamai(self.page))
            should_flush.assert_called_once_with(self.page)


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
