from django.test import TestCase, override_settings

from wagtail.tests.testapp.models import SimplePage
from wagtail.wagtailcore.models import Site

import mock

from v1.wagtail_hooks import (
    RelativePageLinkHandler, check_permissions, form_module_handlers,
)


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


class TestRelativePageLinkHandler(TestCase):
    def setUp(self):
        self.default_site = Site.objects.get(is_default_site=True)

    def test_nonexisting_page_returns_empty_link(self):
        self.assertEqual(
            RelativePageLinkHandler.expand_db_attributes(
                attrs={'id': 0},
                for_editor=False
            ),
            '<a>',
        )

    def test_page_not_in_site_root_returns_none_link(self):
        self.assertEqual(
            RelativePageLinkHandler.expand_db_attributes(
                attrs={'id': 1},
                for_editor=False
            ),
            '<a href="None">',
        )

    def check_page_renders_as_relative_link(self):
        page = SimplePage(title='title', slug='slug', content='content')
        self.default_site.root_page.add_child(instance=page)

        self.assertEqual(
            RelativePageLinkHandler.expand_db_attributes(
                attrs={'id': page.pk},
                for_editor=False
            ),
            '<a href="/slug/">',
        )

    def test_single_site_returns_relative_link(self):
        self.assertEqual(Site.objects.count(), 1)
        self.check_page_renders_as_relative_link()

    def test_multiple_sites_still_returns_relative_link(self):
        Site.objects.create(
            hostname='other',
            root_page=self.default_site.root_page,
            is_default_site=False
        )
        self.check_page_renders_as_relative_link()


class TestServeLatestDraftPage(TestCase):
    def setUp(self):
        self.default_site = Site.objects.get(is_default_site=True)
        self.page = SimplePage(title='live', slug='test', content='test')
        self.default_site.root_page.add_child(instance=self.page)
        self.page.title = 'draft'
        self.page.save_revision()

    @override_settings(SERVE_LATEST_DRAFT_PAGES=[])
    def test_not_serving_draft_serves_published_revision(self):
        response = self.client.get('/test/')
        self.assertContains(response, 'live')
        self.assertIsNone(response.get('Serving-Wagtail-Draft'))

    def test_serving_draft_serves_latest_revision_and_adds_header(self):
        with override_settings(SERVE_LATEST_DRAFT_PAGES=[self.page.pk]):
            response = self.client.get('/test/')
            self.assertContains(response, 'draft')
            self.assertEqual(response['Serving-Wagtail-Draft'], '1')
