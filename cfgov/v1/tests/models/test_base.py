import datetime

from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponseBadRequest
from django.test import TestCase
from django.test.client import RequestFactory

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Site

import mock

from v1.models import BrowsePage, CFGOVPage, Feedback
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

    @mock.patch('__builtin__.super')
    @mock.patch('v1.models.base.hooks')
    def test_get_context_calls_get_context(self, mock_hooks, mock_super):
        self.page.get_context(self.request)
        mock_super.assert_called_with(CFGOVPage, self.page)
        mock_super().get_context.assert_called_with(self.request)

    @mock.patch('__builtin__.super')
    @mock.patch('v1.models.base.hooks')
    def test_get_context_calls_get_hooks(self, mock_hooks, mock_super):
        self.page.get_context(self.request)
        mock_hooks.get_hooks.assert_called_with('cfgovpage_context_handlers')

    @mock.patch('__builtin__.super')
    @mock.patch('v1.models.base.hooks')
    def test_get_context_calls_hook_functions(self, mock_hooks, mock_super):
        fn = mock.Mock()
        mock_hooks.get_hooks.return_value = [fn]
        self.page.get_context(self.request)
        fn.assert_called_with(
            self.page, self.request, mock_super().get_context()
        )

    @mock.patch('__builtin__.super')
    @mock.patch('v1.models.base.hooks')
    def test_get_context_returns_context(self, mock_hooks, mock_super):
        result = self.page.get_context(self.request)
        self.assertEqual(result, mock_super().get_context())

    @mock.patch('__builtin__.super')
    def test_serve_calls_super_on_non_ajax_request(self, mock_super):
        self.page.serve(self.request)
        mock_super.assert_called_with(CFGOVPage, self.page)
        mock_super().serve.assert_called_with(self.request)

    @mock.patch('__builtin__.super')
    @mock.patch('v1.models.base.CFGOVPage.serve_post')
    def test_serve_calls_serve_post_on_post_request(
            self, mock_serve_post, mock_super):
        self.request = self.factory.post('/')
        self.page.serve(self.request)
        mock_serve_post.assert_called_with(self.request)

    def test_serve_post_returns_400_for_no_form_id(self):
        request = self.factory.post('/')
        response = self.page.serve_post(request)
        self.assertIsInstance(response, HttpResponseBadRequest)
        self.assertEqual(response.content, str(self.page.url))

    def test_serve_post_returns_json_400_for_no_form_id(self):
        request = self.factory.post(
            '/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        response = self.page.serve_post(request)
        self.assertEqual(response.content, '{"result": "error"}')
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


class TestFeedbackModel(TestCase):
    def setUp(self):
        self.test_feedback = Feedback(
            email='tester@example.com',
            comment="Sparks on the curb.",
            is_helpful=True,
            referrer="https://www.consumerfinance.gov/owing-a-home/",
            submitted_on=datetime.datetime.now()
        )
        self.test_feedback.save()

    def test_assemble_csv(self):
        test_csv = Feedback().assemble_csv(Feedback.objects.all())
        for term in ["comment",
                     "Sparks on the curb",
                     "tester@example.com",
                     "{}".format(self.test_feedback.submitted_on.date())]:
            self.assertIn(term, test_csv)


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
