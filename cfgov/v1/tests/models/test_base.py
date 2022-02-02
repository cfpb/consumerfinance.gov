import json
from unittest import mock

from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponseBadRequest
from django.test import TestCase
from django.test.client import RequestFactory

from wagtail.core import blocks
from wagtail.core.models import Site

from v1.models import (
    AbstractFilterPage, BrowsePage, CFGOVPage, LandingPage, SublandingPage
)
from v1.models.banners import Banner
from v1.tests.wagtail_pages.helpers import save_new_page


class TestCFGOVPage(TestCase):
    def setUp(self):
        self.page = CFGOVPage(title='Test', slug='test')
        self.factory = RequestFactory()
        self.request = self.factory.get('/')

    def test_post_preview_cache_key_contains_page_id(self):
        save_new_page(self.page)
        key = self.page.post_preview_cache_key
        self.assertIn(str(self.page.id), key)

    @mock.patch('builtins.super')
    def test_serve_calls_super_on_non_ajax_request(self, mock_super):
        self.page.serve(self.request)
        mock_super.assert_called_once()
        mock_super().serve.assert_called_with(self.request)

    @mock.patch('v1.models.base.CFGOVPage.serve_post')
    def test_serve_calls_serve_post_on_post_request(self, mock_serve_post):
        self.request = self.factory.post('/')
        self.page.serve(self.request)
        mock_serve_post.assert_called_with(self.request)

    def test_serve_post_returns_400_for_no_form_id(self):
        request = self.factory.post('/')
        response = self.page.serve_post(request)
        self.assertIsInstance(response, HttpResponseBadRequest)

    def test_serve_post_returns_json_400_for_no_form_id(self):
        request = self.factory.post(
            '/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        response = self.page.serve_post(request)
        self.assertEqual(response.content, b'{"result": "error"}')
        self.assertEqual(response.status_code, 400)

    def test_serve_post_returns_400_for_invalid_form_id_wrong_parts(self):
        request = self.factory.post('/', {'form_id': 'foo'})
        response = self.page.serve_post(request)
        self.assertIsInstance(response, HttpResponseBadRequest)

    def test_serve_post_returns_400_for_invalid_form_id_invalid_field(self):
        request = self.factory.post('/', {'form_id': 'form-foo-2'})
        response = self.page.serve_post(request)
        self.assertIsInstance(response, HttpResponseBadRequest)

    def test_serve_post_returns_400_for_invalid_form_id_invalid_index(self):
        page = BrowsePage(title='test', slug='test')
        request = self.factory.post('/', {'form_id': 'form-content-99'})
        response = page.serve_post(request)
        self.assertIsInstance(response, HttpResponseBadRequest)

    def test_serve_post_returns_400_for_invalid_form_id_non_number_index(self):
        page = BrowsePage(title='test', slug='test')
        request = self.factory.post('/', {'form_id': 'form-content-abc'})
        response = page.serve_post(request)
        self.assertIsInstance(response, HttpResponseBadRequest)

    def test_serve_post_returns_400_for_invalid_form_id_no_form_present(self):
        page = BrowsePage(title='test', slug='test')
        page.content = blocks.StreamValue(
            page.content.stream_block,
            [{'type': 'full_width_text', 'value': []}],
            True
        )
        save_new_page(page)

        request = self.factory.post('/', {'form_id': 'form-content-0'})
        response = page.serve_post(request)
        self.assertIsInstance(response, HttpResponseBadRequest)

    def test_serve_post_valid_calls_feedback_block_handler(self):
        """A valid post should call the feedback block handler.

        This returns a redirect to the calling page and also uses the
        Django messages framework to set a message.
        """
        page = BrowsePage(title='test', slug='test')
        page.content = blocks.StreamValue(
            page.content.stream_block,
            [{'type': 'feedback', 'value': 'something'}],
            True
        )
        save_new_page(page)

        request = self.factory.post('/', {'form_id': 'form-content-0'})
        SessionMiddleware().process_request(request)
        MessageMiddleware().process_request(request)

        response = page.serve_post(request)

        self.assertEqual(
            (response.status_code, response['Location']),
            (302, request.path)
        )

    @mock.patch('v1.models.base.TemplateResponse')
    @mock.patch('v1.models.base.CFGOVPage.get_template')
    @mock.patch('v1.models.base.CFGOVPage.get_context')
    @mock.patch('v1.models.base.getattr')
    def test_serve_post_gets_streamfield_from_page_using_form_id(
            self,
            mock_getattr,
            mock_get_context,
            mock_get_template,
            mock_response):
        mock_getattr.return_value = mock.MagicMock()
        mock_get_context.return_value = mock.MagicMock()
        self.request = self.factory.post(
            '/',
            {'form_id': 'form-content-0'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.page.serve_post(self.request)
        mock_getattr.assert_called_with(self.page, 'content', None)

    @mock.patch('v1.models.base.TemplateResponse')
    @mock.patch('v1.models.base.CFGOVPage.get_template')
    @mock.patch('v1.models.base.CFGOVPage.get_context')
    @mock.patch('v1.models.base.getattr')
    def test_serve_post_calls_module_get_result(
            self,
            mock_getattr,
            mock_get_context,
            mock_get_template,
            mock_response):
        self.request = self.factory.post(
            '/',
            {'form_id': 'form-content-0'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.page.serve_post(self.request)
        module = mock_getattr()[0]
        module.block.get_result.assert_called_with(
            self.page,
            self.request,
            module.value,
            True
        )

    @mock.patch('v1.models.base.isinstance')
    @mock.patch('v1.models.base.TemplateResponse')
    @mock.patch('v1.models.base.CFGOVPage.get_template')
    @mock.patch('v1.models.base.CFGOVPage.get_context')
    @mock.patch('v1.models.base.getattr')
    def test_serve_post_returns_result_if_response(
            self, mock_getattr,
            mock_get_context,
            mock_get_template,
            mock_response,
            mock_isinstance):
        mock_getattr.return_value = mock.MagicMock()
        mock_get_context.return_value = mock.MagicMock()
        self.request = self.factory.post(
            '/',
            {'form_id': 'form-content-0'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        result = self.page.serve_post(self.request)
        module = mock_getattr()[0]
        self.assertEqual(result, module.block.get_result())

    @mock.patch('v1.models.base.TemplateResponse')
    @mock.patch('v1.models.base.CFGOVPage.get_template')
    @mock.patch('v1.models.base.CFGOVPage.get_context')
    @mock.patch('v1.models.base.getattr')
    def test_serve_post_calls_get_context(
            self,
            mock_getattr,
            mock_get_context,
            mock_get_template,
            mock_response):
        mock_getattr.return_value = mock.MagicMock()
        mock_get_context.return_value = mock.MagicMock()
        self.request = self.factory.post(
            '/',
            {'form_id': 'form-content-0'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.page.serve_post(self.request)
        self.assertTrue(mock_get_context.called)

    @mock.patch('v1.models.base.TemplateResponse')
    @mock.patch('v1.models.base.CFGOVPage.get_template')
    @mock.patch('v1.models.base.CFGOVPage.get_context')
    @mock.patch('v1.models.base.getattr')
    def test_serve_post_sets_context(
            self,
            mock_getattr,
            mock_get_context,
            mock_get_template,
            mock_response):
        context = {'form_modules': {'content': {}}}
        mock_getattr.return_value = mock.MagicMock()
        mock_get_context.return_value = context
        self.request = self.factory.post(
            '/',
            {'form_id': 'form-content-0'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.page.serve_post(self.request)
        module = mock_getattr()[0]
        self.assertIn(0, context['form_modules']['content'])
        self.assertEqual(
            module.block.get_result(), context['form_modules']['content'][0]
        )

    @mock.patch('v1.models.base.TemplateResponse')
    @mock.patch('v1.models.base.CFGOVPage.get_template')
    @mock.patch('v1.models.base.CFGOVPage.get_context')
    @mock.patch('v1.models.base.getattr')
    def test_serve_post_returns_template_response_if_result_not_response(
            self,
            mock_getattr,
            mock_get_context,
            mock_get_template,
            mock_response):
        mock_getattr.return_value = mock.MagicMock()
        mock_get_context.return_value = mock.MagicMock()
        self.request = self.factory.post(
            '/',
            {'form_id': 'form-content-0'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        result = self.page.serve_post(self.request)
        mock_response.assert_called_with(
            self.request, mock_get_template(), mock_get_context()
        )
        self.assertEqual(result, mock_response())

    def test_archived_property(self):
        # Test default value of is_archived results in False property
        self.assertFalse(self.page.archived)

        self.page.is_archived = 'no'
        self.assertFalse(self.page.archived)

        self.page.is_archived = 'never'
        self.assertFalse(self.page.archived)

        self.page.is_archived = 'yes'
        self.assertTrue(self.page.archived)


class TestCFGOVPageContext(TestCase):
    def setUp(self):
        self.page = CFGOVPage(title='Test', slug='test')
        self.factory = RequestFactory()
        self.request = self.factory.get('/')

    def test_post_preview_cache_key_contains_page_id(self):
        save_new_page(self.page)
        key = self.page.post_preview_cache_key
        self.assertIn(str(self.page.id), key)

    @mock.patch('v1.models.base.hooks.get_hooks')
    def test_get_context_calls_get_hooks(self, mock_get_hooks):
        self.page.get_context(self.request)
        mock_get_hooks.assert_called_with('cfgovpage_context_handlers')

    def test_get_context_no_banners(self):
        test_context = self.page.get_context(self.request)
        self.assertFalse(test_context['banners'])

    def test_get_context_one_banner_not_matching(self):
        Banner.objects.create(title='Banner', url_pattern='foo', enabled=True)
        test_context = self.page.get_context(self.request)
        self.assertFalse(test_context['banners'])

    def test_get_context_one_banner_matching(self):
        Banner.objects.create(title='Banner', url_pattern='/', enabled=True)
        test_context = self.page.get_context(self.request)
        self.assertTrue(test_context['banners'])

    def test_get_context_one_banner_matching_disabled(self):
        Banner.objects.create(title='Banner', url_pattern='/', enabled=False)
        test_context = self.page.get_context(self.request)
        self.assertFalse(test_context['banners'])

    def test_get_context_multiple_banners_matching(self):
        Banner.objects.create(title='Banner', url_pattern='/', enabled=True)
        Banner.objects.create(title='Banner2', url_pattern='/', enabled=True)
        Banner.objects.create(title='Banner3', url_pattern='/', enabled=False)
        Banner.objects.create(title='Banner4', url_pattern='foo', enabled=True)
        test_context = self.page.get_context(self.request)
        self.assertEqual(test_context['banners'].count(), 2)

    def test_get_context_no_schema_json(self):
        test_context = self.page.get_context(self.request)
        self.assertNotIn('schema_json', test_context)

    def test_get_context_with_schema_json(self):
        self.page.schema_json = {
            "@type": "SpecialAnnouncement",
            "@context": "http://schema.org",
            "category": "https://www.wikidata.org/wiki/Q81068910",
            "name": "Special announcement headline",
            "text": "Special announcement details",
            "datePosted": "2020-03-17",
            "expires": "2020-03-24"
        }
        test_context = self.page.get_context(self.request)
        self.assertIn('schema_json', test_context)

    def test_get_context_sets_meta_description_from_search_description(self):
        result = 'Correct Meta Description'
        self.page = LandingPage(
            title='test',
            search_description=result,
            header=json.dumps(
                [
                    {
                        "type": "hero",
                        "value": {
                            "body": 'Incorrect Meta Description'
                        },
                    }
                ]
            ),)
        test_context = self.page.get_context(self.request)
        self.assertEqual(test_context['meta_description'], result)

    def test_get_context_sets_meta_description_from_hero(self):
        expected = 'Correct Meta Description'
        self.page = LandingPage(
            title='test',
            header=json.dumps(
                [
                    {
                        "type": "text_introduction",
                        "value": {
                            "intro": 'Incorrect Meta Description'
                        },
                    },
                    {
                        "type": "hero",
                        "value": {
                            "body": expected
                        },
                    }
                ]
            ),
            content=json.dumps(
                [
                    {
                        "type": "text_introduction",
                        "value": {
                            "intro": 'Incorrect Meta Description'
                        }
                    }
                ]
            )
        )
        test_context = self.page.get_context(self.request)
        result = test_context['meta_description']
        self.assertEqual(expected, result)

    def test_get_context_sets_meta_description_from_preview_description(self):
        expected = 'Correct Meta Description'
        self.page = AbstractFilterPage(
            title='test',
            preview_description="<p>" + expected + "</p>",
            header=json.dumps(
                [
                    {
                        "type": "text_introduction",
                        "value": {
                            "intro": 'Incorrect Meta Description'
                        },
                    },
                ]
            )
        )
        test_context = self.page.get_context(self.request)
        result = test_context['meta_description']
        self.assertEqual(" " + expected + " ", result)

    def test_get_context_sets_meta_description_from_header_text_introduction_intro(self):  # noqa
        expected = 'Correct Meta Description'
        self.page = LandingPage(
            title='test',
            header=json.dumps(
                [
                    {
                        "type": "text_introduction",
                        "value": {
                            "intro": expected
                        },
                    },
                    {
                        "type": "text_introduction",
                        "value": {
                            "intro": 'Incorrect Meta Description'
                        },
                    },
                ]
            ),
            content=json.dumps(
                [
                    {
                        "type": "text_introduction",
                        "value": {
                            "intro": 'Incorrect Meta Description'
                        }
                    }
                ]
            )
        )
        test_context = self.page.get_context(self.request)
        result = test_context['meta_description']
        self.assertEqual(expected, result)

    def test_get_context_sets_meta_description_from_content_text_introduction_intro(self):  # noqa
        expected = 'Correct Meta Description'
        self.page = SublandingPage(
            title='test',
            header=json.dumps(
                [
                    {
                        "type": "text_introduction",
                        "value": {
                            "body": 'Incorrect Meta Description'
                        }
                    },
                ]
            ),
            content=json.dumps(
                [
                    {
                        "type": "text_introduction",
                        "value": {
                            "intro": expected
                        }
                    }
                ]
            )
        )
        test_context = self.page.get_context(self.request)
        result = test_context['meta_description']
        self.assertEqual(expected, result)

    def test_get_context_sets_meta_description_from_header_item_introduction_paragraph(self):  # noqa
        expected = 'Correct Meta Description'
        self.page = AbstractFilterPage(
            title='test',
            header=json.dumps(
                [
                    {
                        "type": "item_introduction",
                        "value": {
                            "paragraph": expected
                        }
                    },
                ]
            )
        )
        test_context = self.page.get_context(self.request)
        result = test_context['meta_description']
        self.assertEqual(expected, result)

    def test_get_context_sets_meta_description_to_blank_if_no_other_data_to_set(self):  # noqa
        expected = ''
        self.page = SublandingPage(
            title='test',
            content=json.dumps(
                [
                    {
                        "type": "notification",
                        "value": {
                            "body": 'Incorrect Meta Description'
                        }
                    }
                ]
            )
        )
        test_context = self.page.get_context(self.request)
        result = test_context['meta_description']
        self.assertEqual(expected, result)

    def test_get_context_sets_meta_description_strips_html_tags(self):
        expected = 'Correct Meta Description'
        self.page = SublandingPage(
            title='test',
            header=json.dumps(
                [
                    {
                        "type": "hero",
                        "value": {
                            "body": '<p></li>' + expected + '</li></p>'
                        }
                    }
                ]
            )
        )
        test_context = self.page.get_context(self.request)
        result = test_context['meta_description']
        expectedWithSpaces = '  ' + expected + '  '
        self.assertEqual(expectedWithSpaces, result)


class TestCFGOVPageQuerySet(TestCase):
    def setUp(self):
        default_site = Site.objects.get(is_default_site=True)
        self.live_host = default_site.hostname

    def check_live_counts(self, on_live_host):
        pages = CFGOVPage.objects
        self.assertEqual(
            pages.live().count(),
            on_live_host
        )

    def test_live_with_only_root_page(self):
        self.check_live_counts(on_live_host=1)

    def test_live_with_another_draft_page(self):
        page = CFGOVPage(title='test', slug='test', live=False)
        save_new_page(page)
        self.check_live_counts(on_live_host=1)

    def test_live_with_another_live_page(self):
        page = CFGOVPage(title='test', slug='test', live=True)
        save_new_page(page)
        self.check_live_counts(on_live_host=2)


class TestCFGOVPageMediaProperty(TestCase):
    """Tests how the page.media property pulls in child block JS."""
    def test_empty_page_has_no_media(self):
        return self.assertEqual(CFGOVPage().media, [])

    def test_empty_page_has_no_page_js(self):
        return self.assertEqual(CFGOVPage().page_js, [])

    def test_empty_page_has_no_streamfield_js(self):
        return self.assertEqual(CFGOVPage().streamfield_js, [])

    def test_page_pulls_in_child_block_media(self):
        page = CFGOVPage()
        page.sidefoot = blocks.StreamValue(
            page.sidefoot.stream_block,
            [
                {
                    'type': 'email_signup',
                    'value': {'heading': 'Heading'}
                },
            ],
            True
        )

        self.assertEqual(page.media, ['email-signup.js'])

    def test_doesnt_pull_in_media_for_nonexistent_child_blocks(self):
        page = BrowsePage()
        page.content = blocks.StreamValue(
            page.content.stream_block,
            [
                {
                    'type': 'full_width_text',
                    'value': [],
                },
            ],
            True
        )

        # The page media should only include the default BrowsePae media, and
        # shouldn't add any additional files because of the FullWithText.
        self.assertEqual(page.media, ['secondary-navigation.js'])


class TestCFGOVPageCopy(TestCase):

    def setUp(self):
        self.site = Site.objects.first()
        self.root_page = self.site.root_page
        self.page_with_tags = CFGOVPage(
            title='Tagged',
            slug='tagged',
            live=True
        )
        save_new_page(self.page_with_tags, root=self.root_page)
        self.page_with_tags.tags.add('tag1')
        self.page_with_tags.authors.add('author1')
        self.page_with_tags.save()

    def check_tagged_page_copies_without_error(self):
        test_page = self.page_with_tags
        new_page = test_page.copy(
            update_attrs={
                "slug": f"{test_page.slug}-copy",
                "title": f"{test_page.title} COPY"
            }
        )
        self.assertEqual(
            new_page.title, "Tagged COPY")


class TestCFGOVPageBreadcrumbs(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        self.site = Site.objects.first()
        self.root_page = self.site.root_page

        self.top_level_page = CFGOVPage(
            title='top',
            slug='top',
            live=True
        )
        save_new_page(self.top_level_page, root=self.root_page)

        self.second_level_page = CFGOVPage(
            title='second',
            slug='second',
            live=True
        )
        save_new_page(self.second_level_page, root=self.top_level_page)

        self.third_level_page = CFGOVPage(
            title='third',
            slug='third',
            live=True
        )
        save_new_page(self.third_level_page, root=self.second_level_page)

    def test_get_breadcrumbs_forced_homepage_descendant(self):
        request = self.factory.get('/top/second')
        self.top_level_page.force_breadcrumbs = True
        self.top_level_page.save()
        self.assertIn(
            'top',
            [p.slug for p in self.second_level_page.get_breadcrumbs(request)]
        )

    def test_get_breadcrumbs_no_homepage_descendant(self):
        request = self.factory.get('/top/second')
        self.assertNotIn(
            'top',
            [p.slug for p in self.second_level_page.get_breadcrumbs(request)]
        )

    def test_get_breadcrumbs_two_levels_deep(self):
        request = self.factory.get('/top/second/third')
        self.assertNotIn(
            'top',
            [p.slug for p in self.third_level_page.get_breadcrumbs(request)]
        )
        self.assertIn(
            'second',
            [p.slug for p in self.third_level_page.get_breadcrumbs(request)]
        )
