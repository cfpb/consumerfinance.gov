import mock
import json

from django.test import TestCase
from django.test.client import RequestFactory

from ..wagtail_hooks import share_the_page, check_permissions, share, configure_page_revision


class TestShareThePage(TestCase):

    @mock.patch('wagtail.wagtailcore.hooks.register')
    def setUp(self, mock_register):
        from ..wagtail_hooks import share_the_page
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
    def test_save_draft(self, mock_configure_page_revision, mock_share, mock_check_permissions, mock_page):
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
    def test_share_on_content(self, mock_configure_page_revision, mock_share, mock_check_permissions, mock_page):
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
    def test_publish_to_www(self, mock_configure_page_revision, mock_share, mock_check_permissions, mock_page):
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
    def test_function_calls(self, mock_configure_page_revision, mock_share, mock_check_permissions, mock_page):
        """
            Make sure all functions are called once.
        """
        mock_page.objects.get.return_value = self.page
        share_the_page(self.mock_request['publishing'], self.page)
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
        revision = mock.Mock()
        revision.content_json = '{"live": false, "shared": false}'
        self.page.get_latest_revision.return_value = revision
        self.page.live, self.page.shared = False, False

    def test_calls_get_latest_revision(self):
        configure_page_revision(self.page, False)
        assert self.page.get_latest_revision.called

    def test_calls_save(self):
        configure_page_revision(self.page, False)
        revision = self.page.get_latest_revision()
        assert revision.save.called

    def test_calls_publish(self):
        configure_page_revision(self.page, True)
        revision = self.page.get_latest_revision()
        assert revision.publish.called

    def test_does_not_call_publish(self):
        configure_page_revision(self.page, False)
        revision = self.page.get_latest_revision()
        assert not revision.publish.called

    def test_save_a_draft(self):
        configure_page_revision(self.page, False)
        latest = self.page.get_latest_revision()
        latest_content = json.loads(latest.content_json)
        assert not self.page.shared
        assert not self.page.live
        assert not latest_content['shared']
        assert not latest_content['live']

    def test_sharing_a_page(self):
        self.page.shared = True
        configure_page_revision(self.page, False)
        latest = self.page.get_latest_revision()
        latest_content = json.loads(latest.content_json)
        assert self.page.shared
        assert not self.page.live
        assert latest_content['shared']
        assert not latest_content['live']

    def test_publishing_a_page(self):
        self.page.shared = True
        self.page.live = True
        configure_page_revision(self.page, True)
        latest = self.page.get_latest_revision()
        latest_content = json.loads(latest.content_json)
        assert self.page.shared
        assert self.page.live
        assert latest_content['shared']
        assert latest_content['live']
