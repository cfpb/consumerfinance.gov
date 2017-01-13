import datetime

import mock
from django.test import TestCase
from django.test.client import RequestFactory
from wagtail.wagtailcore.models import Site

from v1.models.base import CFGOVPage, Feedback
from v1.tests.wagtail_pages.helpers import publish_page, save_new_page


class TestCFGOVPage(TestCase):
    def setUp(self):
        self.page = CFGOVPage(title='Test', slug='test')
        self.factory = RequestFactory()
        self.request = self.factory.get('/')

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

    def test_serve_post_returns_failed_JSON_response_for_no_form_id(self):
        self.request = self.factory.post(
            '/', HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        response = self.page.serve_post(self.request)
        self.assertEqual(response.content, '{"result": "error"}')
        self.assertEqual(response.status_code, 400)

    @mock.patch('v1.models.base.HttpResponseBadRequest')
    def test_serve_post_calls_messages_and_bad_request_for_no_form_id(
            self, mock_bad_request):
        self.request = self.factory.post('/')
        self.page.serve_post(self.request)
        mock_bad_request.assert_called_with(self.page.url)

    @mock.patch('v1.models.base.HttpResponseBadRequest')
    def test_serve_post_returns_bad_request_for_no_form_id(
            self, mock_bad_request):
        self.request = self.factory.post('/')
        self.page.serve_post(self.request)
        self.assertTrue(mock_bad_request.called)

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
        mock_getattr.assert_called_with(self.page, 'content')

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

        staging_site = Site.objects.get(is_default_site=False)
        self.staging_host = staging_site.hostname

    def check_live_shared_counts(self, on_live_host, on_staging_host):
        pages = CFGOVPage.objects
        self.assertEqual(
            pages.live_shared(hostname=self.live_host).count(),
            on_live_host
        )
        self.assertEqual(
            pages.live_shared(hostname=self.staging_host).count(),
            on_staging_host
        )

    def test_live_shared_with_only_root_page(self):
        self.check_live_shared_counts(on_live_host=1, on_staging_host=1)

    def test_live_shared_with_another_draft_page(self):
        page = CFGOVPage(title='test', slug='test', live=False, shared=False)
        save_new_page(page)
        self.check_live_shared_counts(on_live_host=1, on_staging_host=1)

    def test_live_shared_with_another_shared_page(self):
        page = CFGOVPage(title='test', slug='test', live=False, shared=True)
        save_new_page(page)
        self.check_live_shared_counts(on_live_host=1, on_staging_host=2)

    def test_live_shared_with_another_live_page(self):
        page = CFGOVPage(title='test', slug='test', live=True, shared=False)
        save_new_page(page)
        self.check_live_shared_counts(on_live_host=2, on_staging_host=2)

    def test_live_shared_with_another_live_shared_page(self):
        page = CFGOVPage(title='test', slug='test', live=True, shared=True)
        publish_page(page)
        self.check_live_shared_counts(on_live_host=2, on_staging_host=2)


class TestFeedbackModel(TestCase):
    def setUp(self):
        self.test_feedback = Feedback(
            email='tester@example.com',
            comment="Sparks on the curb.",
            is_helpful=True,
            referrer="http://www.consumerfinance.gov/owing-a-home/",
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


class CFGOVPageStatusStringTest(TestCase):
        def test_expired(self):
            page = CFGOVPage(expired=True)
            self.assertEqual(page.status_string, 'expired')

        def test_live(self):
            page = CFGOVPage(live=True)
            self.assertEqual(page.status_string, 'live')

        def test_draft(self):
            page = CFGOVPage(live=False, shared=False)
            self.assertEqual(page.status_string, 'draft')

        def test_shared(self):
            page = CFGOVPage(live=False, shared=True)
            self.assertEqual(page.status_string, 'shared')

        def test_live_and_shared(self):
            page = CFGOVPage(
                live=True,
                shared=True,
                has_unpublished_changes=True
            )
            self.assertEqual(page.status_string, 'live + shared')
