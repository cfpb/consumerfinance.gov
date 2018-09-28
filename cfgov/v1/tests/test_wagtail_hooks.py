from django.core.cache import cache, caches
from django.test import TestCase, override_settings

from wagtail.tests.testapp.models import SimplePage
from wagtail.wagtailcore.models import Site

import mock

from v1.models.base import CFGOVPage
from v1.models.menu_item import MenuItem
from v1.models.resources import Resource
from v1.wagtail_hooks import (
    check_permissions, form_module_handlers, get_resource_tags
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

class TestMenuItemSave(TestCase):
    @override_settings(
        CACHES = {
            'default_fragment_cache': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            }
        })
    def test_mega_menu_cache_cleared(self):
        caches['default_fragment_cache'].set('mega_menu', 'menu_content')
        self.assertEqual(
            caches['default_fragment_cache'].get('mega_menu'),
            'menu_content'
        )
        menu_item = MenuItem()
        menu_item.save()
        self.assertEqual(
            caches['default_fragment_cache'].get('mega_menu'),
            None
        )


class TestResourcesModelAdmin(TestCase):
    def setUp(self):
        self.resource1 = Resource.objects.create(title='Test resource 1')
        self.resource1.tags.add(u'tagA')
        self.resource2 = Resource.objects.create(title='Test resource 2')
        self.resource2.tags.add(u'tagB')
        self.page1 = CFGOVPage(title='live', slug='test')
        self.page1.tags.add(u'tagC')

    def test_get_resource_tags_returns_only_resource_tags(self):
        self.assertEqual(
            get_resource_tags(),
            [(u'taga', u'tagA'), (u'tagb', u'tagB')]
        )

    def test_get_resource_tags_returns_only_unique_tags(self):
        self.resource2.tags.add(u'tagA')
        self.assertEqual(
            get_resource_tags(),
            [(u'taga', u'tagA'), (u'tagb', u'tagB')]
        )

    def test_get_resource_tags_returns_alphabetized_list(self):
        self.resource1.tags.add(u'aTag')
        self.assertEqual(
            get_resource_tags(),
            [(u'atag', u'aTag'), (u'taga', u'tagA'), (u'tagb', u'tagB')]
        )
