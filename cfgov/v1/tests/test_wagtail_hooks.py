import unittest
from unittest import mock

from django.test import (
    RequestFactory, SimpleTestCase, TestCase, override_settings
)

from wagtail.core.models import Site
from wagtail.core.whitelist import Whitelister as Allowlister
from wagtail.tests.testapp.models import SimplePage
from wagtail.tests.utils import WagtailTestUtils

from v1.models.base import CFGOVPage
from v1.models.resources import Resource
from v1.wagtail_hooks import (
    form_module_handlers, get_resource_tags, set_served_by_wagtail_sharing
)


class TestFormModuleHandlers(TestCase):
    def setUp(self):
        mock.patch('v1.wagtail_hooks.hooks.register')
        self.page = mock.Mock()
        self.request = mock.Mock()
        self.context = {}

    @mock.patch('builtins.hasattr')
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

    @mock.patch('builtins.hasattr')
    @mock.patch('v1.wagtail_hooks.util.get_streamfields')
    def test_checks_child_block_if_set_form_context_exists(
            self, mock_getstreamfields, mock_hasattr):
        child = mock.Mock()
        streamfields = {'name': [child]}
        mock_getstreamfields.return_value = streamfields
        form_module_handlers(self.page, self.request, self.context)
        mock_hasattr.assert_called_with(child.block, 'get_result')

    @mock.patch('builtins.hasattr')
    @mock.patch('v1.wagtail_hooks.util.get_streamfields')
    def test_sets_context_fieldname_if_not_set(
            self, mock_getstreamfields, mock_hasattr):
        child = mock.Mock()
        streamfields = {'name': [child]}
        mock_getstreamfields.return_value = streamfields
        mock_hasattr.return_value = True
        form_module_handlers(self.page, self.request, self.context)
        assert 'name' in self.context['form_modules']
        self.assertIsInstance(self.context['form_modules']['name'], dict)

    @mock.patch('builtins.hasattr')
    @mock.patch('v1.wagtail_hooks.util.get_streamfields')
    def test_calls_child_block_get_result(
            self, mock_getstreamfields, mock_hasattr):
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

    @mock.patch('builtins.hasattr')
    @mock.patch('v1.wagtail_hooks.util.get_streamfields')
    def test_calls_child_block_is_submitted(
            self, mock_getstreamfields, mock_hasattr):
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


class TestGetResourceTags(TestCase):
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


class TestResourceTagsFilter(TestCase, WagtailTestUtils):
    def setUp(self):
        self.login()
        self.resource1 = Resource.objects.create(
            title='Test resource Orange',
            order=1
        )
        self.resource1.tags.add(u'tagA')
        self.resource2 = Resource.objects.create(
            title='Test resource Banana',
            order=2
        )
        self.resource2.tags.add(u'tagB')
        self.resource3 = Resource.objects.create(
            title='Test resource Apple',
            order=3
        )
        self.resource3.tags.add(u'tagB')
        self.resource3.tags.add(u'tagC')

    def get(self, **params):
        return self.client.get('/admin/v1/resource/', params)

    def test_no_params_returns_all_resources_in_order(self):
        response = self.get()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['result_count'], 3)
        self.assertEqual(
            list(response.context['object_list']),
            list(Resource.objects.all().order_by('title'))
        )

    def test_tag_param_returns_a_resource_tagged_that_way(self):
        response = self.get(tag='taga')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['result_count'], 1)

        for resource in response.context['object_list']:
            self.assertEqual(resource.title, 'Test resource Orange')

    def test_tag_param_returns_resources_tagged_that_way(self):
        response = self.get(tag='tagb')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['result_count'], 2)
        self.assertEqual(
            response.context['object_list'][0].title,
            'Test resource Apple'
        )
        self.assertEqual(
            response.context['object_list'][1].title,
            'Test resource Banana'
        )


class TestAllowlistOverride(SimpleTestCase):
    # Borrowed from https://github.com/wagtail/wagtail/blob/master/wagtail
    # /core/tests/test_whitelist.py

    def setUp(self):
        self.allowlister = Allowlister()

    def test_allowlist_hooks(self):
        """
        Allowlister.clean should remove disallowed tags and attributes from
        a string
        """
        input_html = '<scan class="id">Consumer <embed>Finance</embed></scan>'
        output_html = self.allowlister.clean(input_html)
        self.assertHTMLEqual(output_html, 'Consumer Finance')


class TestSetServedByWagtailSharing(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_set_served_by_wagtail_sharing(self):
        request = self.factory.get('/an-url')
        set_served_by_wagtail_sharing(None, request, [], {})
        self.assertTrue(request.served_by_wagtail_sharing)
