# -*- coding: utf-8 -*-
from unittest import mock

from django.http import HttpResponse
from django.test import (
    RequestFactory, SimpleTestCase, TestCase, override_settings
)
from django.utils import translation

from bs4 import BeautifulSoup

from core.middleware import (
    DeactivateTranslationsMiddleware, ParseLinksMiddleware,
    PathBasedCsrfViewMiddleware, SelfHealingMiddleware, parse_links
)
from v1.models import CFGOVPage
from v1.tests.wagtail_pages.helpers import publish_page


class TestDownstreamCacheControlMiddleware(TestCase):

    def test_edge_control_header_in_response(self):
        response = self.client.get('/', CSRF_COOKIE='', CSRF_COOKIE_USED=True)
        self.assertIn('Edge-Control', response)

    def test_edge_control_header_not_in_response(self):
        response = self.client.get('/')
        self.assertNotIn('Edge-Control', response)


@mock.patch('core.middleware.parse_links')
class TestParseLinksMiddleware(TestCase):
    def test_parse_links_gets_called(self, mock_parse_links):
        """Middleware correctly invokes parse links when rendering webpage"""
        self.client.get('/')
        mock_parse_links.assert_called_once()

    @override_settings(PARSE_LINKS_EXCLUSION_LIST=[r'^/'])
    def test_parse_links_does_not_get_called_excluded(self, mock_parse_links):
        """Middleware does not invoke parse links when path is excluded"""
        self.client.get('/')
        mock_parse_links.assert_not_called()


class TestShouldParseLinks(TestCase):
    def test_should_not_parse_links_if_non_html(self):
        self.assertFalse(ParseLinksMiddleware.should_parse_links(
            request_path='/foo/bar',
            response_content_type='application/json'
        ))

    def test_should_not_parse_links_if_empty(self):
        self.assertFalse(ParseLinksMiddleware.should_parse_links(
            request_path='/foo/bar',
            response_content_type=''
        ))

    def test_should_parse_links_if_html(self):
        self.assertTrue(ParseLinksMiddleware.should_parse_links(
            request_path='/foo/bar',
            response_content_type='text/html'
        ))

    def check_should_parse_links_for_path(self, path, expected):
        self.assertEqual(
            ParseLinksMiddleware.should_parse_links(
                request_path=path,
                response_content_type='text/html'
            ),
            expected
        )

    def test_should_parse_links_false_for_admin_root(self):
        self.check_should_parse_links_for_path('/admin/', False)

    def test_should_parse_links_false_for_admin_page(self):
        self.check_should_parse_links_for_path('/admin/foo/bar/', False)

    def test_should_parse_links_true_for_admin_page_preview(self):
        self.check_should_parse_links_for_path(
            '/admin/pages/1234/edit/preview/',
            True
        )

    def test_should_parse_links_true_for_admin_page_view_draft(self):
        self.check_should_parse_links_for_path(
            '/admin/pages/1234/view_draft/',
            True
        )


class TestParseLinks(TestCase):
    def test_relative_link_remains_unmodified(self):
        self.assertEqual(
            parse_links('<body><a href="/something">text</a></body>'),
            '<body><a href="/something">text</a></body>'
        )

    def test_works_properly_on_bytestrings(self):
        self.assertEqual(
            parse_links(b'<body><a href="/something">text</a></body>'),
            '<body><a href="/something">text</a></body>'
        )

    def test_non_gov_link(self):
        """Non gov links get external link icon and redirect."""
        link = '<body><a href="https://google.com">external link</a></body>'
        output = parse_links(link)
        self.assertIn('external-site', output)
        self.assertIn('cf-icon-svg', output)

    def test_gov_link(self):
        """Gov links get external link icon but not redirect."""
        link = '<body><a href="https://www.fdic.gov/bar">gov link</a></body>'
        output = parse_links(link)
        self.assertIn('cf-icon-svg', output)

    def test_internal_link(self):
        """Internal links get neither icon nor redirect."""
        link = '''
        <body>
            <a href="https://www.consumerfinance.gov/foo">cfpb link</a>
        </body>
        '''
        output = parse_links(link)
        self.assertNotIn('external-site', output)
        self.assertNotIn('cf-icon-svg', output)

    def test_files_get_download_icon(self):
        file_types = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'csv', 'zip']
        for file_type in file_types:
            link = f'<body><a href="/something.{file_type}">link</a></body>'
            output = parse_links(link)
            self.assertIn('cf-icon-svg', output)

    def test_different_case_pdf_link_gets_download_icon(self):
        link = '<body><a href="/something.PDF">link</a></body>'
        output = parse_links(link)
        self.assertIn('cf-icon-svg', output)

    def test_rich_text_links_get_expanded(self):
        page = CFGOVPage(title='foo bar', slug='foo-bar')
        publish_page(page)
        link = f'<body><a id="{page.id}" linktype="page">foo bar</a></body>'
        output = parse_links(link)
        self.assertEqual(
            '<body><a href="/foo-bar/">foo bar</a></body>',
            output
        )

    def test_non_default_encoding(self):
        s = '<body><a href="/something">哈哈</a></body>'
        encoding = 'gb2312'
        parsed = parse_links(s.encode(encoding), encoding=encoding)
        self.assertEqual(parsed, s)

    def test_external_link_outside_body(self):
        s = '''
        <a href="https://somewhere/foo">Link</a>
        <body>
        </body>
        '''
        output = parse_links(s)
        self.assertNotIn('external-site', output)
        self.assertNotIn('cf-icon-svg', output)

    def test_external_link_outside_body_with_attributes(self):
        s = '''
        <a href="https://somewhere/foo">Link</a>
        <body class="test">
        </body>
        '''
        output = parse_links(s)
        self.assertNotIn('external-site', output)
        self.assertNotIn('cf-icon-svg', output)

    def test_external_link_with_attribute(self):
        s = '''
        <body>
            <a href="https://somewhere" data-thing="something">Link</a>
        </body>
        '''
        output = parse_links(s)
        self.assertIn('external-site', output)
        self.assertIn('cf-icon-svg', output)

    def test_external_link_with_img(self):
        s = '<body><a href="https://somewhere"><img src="some.png"></a></body>'
        output = parse_links(s)
        self.assertIn('external-site', output)
        self.assertNotIn('cf-icon-svg', output)

    def test_external_link_with_background_img(self):
        s = '''
        <body>
            <a href="https://somewhere"><span>
                <div style="background-image: url(\'some.png\')"></div>
            </span></a>
        </body>
        '''
        output = parse_links(s)
        self.assertIn('external-site', output)
        self.assertNotIn('cf-icon-svg', output)

    def test_external_link_with_header(self):
        s = '<body><a href="https://somewhere"><h3>Header</h3></a></body>'
        output = parse_links(s)
        self.assertIn('external-site', output)
        self.assertNotIn('cf-icon-svg', output)

    def test_multiline_external_gov_link(self):
        s = '''
        <body>
            <a class="m-list_link a-link"
               href="https://usa.gov/">
                <span>USA
                .gov</span>
            </a>
        </body>
        '''
        output = parse_links(s)
        self.assertIn('cf-icon-svg', output)

    def test_multiple_links(self):
        s = '''
        <body>
            <a href="https://first.com">one</a>
            <a href="https://second.com">two</a>
        </body>
        '''
        output = parse_links(s)
        soup = BeautifulSoup(output, 'html.parser')
        self.assertEqual(len(soup.find_all('a')), 2)

    def check_after_parse_links_has_this_many_svgs(self, count, s):
        output = parse_links(s)
        soup = BeautifulSoup(output, 'html.parser')
        self.assertEqual(len(soup.find_all('svg')), count)

    def test_link_ending_with_svg_doesnt_get_another_svg(self):
        self.check_after_parse_links_has_this_many_svgs(
            1,
            '<body>'
            '<a href="https://external.gov">'
            '<span>Text before icon</span>'
            '<svg>something</svg>'
            '</a>'
            '</body>'
        )

    def test_link_ending_with_svg_and_whitespace_doesnt_get_another_svg(self):
        self.check_after_parse_links_has_this_many_svgs(
            1,
            '<body>'
            '<a href="https://external.gov">'
            '<span>Text before icon</span> '
            '<svg>something</svg>   \n\t'
            '</a>'
            '</body>'
        )

    def test_with_svg_not_at_the_end_still_gets_svg(self):
        self.check_after_parse_links_has_this_many_svgs(
            2,
            '<body>'
            '<a href="https://external.gov">'
            '<span><svg>something</svg> Text after icon</span>'
            '</a>'
            '</body>'
        )

    def test_with_svg_then_span_still_gets_svg(self):
        self.check_after_parse_links_has_this_many_svgs(
            2,
            '<body>'
            '<a href="https://external.gov">'
            '<svg>something</svg>'
            '<span>Text after icon</span>'
            '</a>'
            '</body>'
        )

    def test_in_page_anchor_links_have_current_path_stripped(self):
        s = '<body><a href="/foo/bar/#anchor">Anchor</a></body>'
        output = parse_links(s, request_path='/foo/bar/')
        self.assertNotIn('/foo/bar/', output)
        self.assertIn('href="#anchor"', output)


class DeactivateTranslationsMiddlewareTests(SimpleTestCase):
    def test_deactivates_translations(self):
        translation.activate('en-us')
        self.assertEqual(translation.get_language(), 'en-us')

        translation.activate('es')
        self.assertEqual(translation.get_language(), 'es')

        def get_response(request):
            pass

        middleware = DeactivateTranslationsMiddleware(get_response)
        request = RequestFactory().get('/')
        middleware(request)

        self.assertEqual(translation.get_language(), 'en-us')


class SelfHealingMiddlewareTests(SimpleTestCase):
    def test_selfhealing_middleware_does_not_redirect_good_urls(self):
        def get_response(request):
            return HttpResponse(status=404)

        middleware = SelfHealingMiddleware(get_response)
        request = RequestFactory().get('/test')
        response = middleware(request)
        self.assertEqual(response.status_code, 404)

    def test_selfhealing_middleware_lowercases_mixed_case_urls(self):
        def get_response(request):
            return HttpResponse(status=404)

        middleware = SelfHealingMiddleware(get_response)
        request = RequestFactory().get('/TEst')
        response = middleware(request)
        self.assertRedirects(
            response,
            '/test',
            status_code=301,
            fetch_redirect_response=False
        )

    def test_selfhealing_middleware_strips_one_extraneous_char(self):
        def get_response(request):
            return HttpResponse(status=404)

        middleware = SelfHealingMiddleware(get_response)
        request = RequestFactory().get('/test)')
        response = middleware(request)
        self.assertRedirects(
            response,
            '/test',
            status_code=301,
            fetch_redirect_response=False
        )

    def test_selfhealing_middleware_strips_two_extraneous_chars(self):
        def get_response(request):
            return HttpResponse(status=404)

        middleware = SelfHealingMiddleware(get_response)
        request = RequestFactory().get('/test )')
        response = middleware(request)
        self.assertRedirects(
            response,
            '/test',
            status_code=301,
            fetch_redirect_response=False
        )

    def test_selfhealing_middleware_strips_all_extraneous_chars(self):
        def get_response(request):
            return HttpResponse(status=404)

        middleware = SelfHealingMiddleware(get_response)
        request = RequestFactory().get(
            '/test ~!@#$%^&*()-_–—=+[]{}\\|;:\'‘’"“”,.…<>?'
        )
        response = middleware(request)
        self.assertRedirects(
            response,
            '/test',
            status_code=301,
            fetch_redirect_response=False
        )

    def test_selfhealing_middleware_lowercase_and_strip_extraneous_chars(self):
        def get_response(request):
            return HttpResponse(status=404)

        middleware = SelfHealingMiddleware(get_response)
        request = RequestFactory().get('/TEst )')
        response = middleware(request)
        self.assertRedirects(
            response,
            '/test',
            status_code=301,
            fetch_redirect_response=False
        )


class PathBasedCsrfViewMiddlewareTestCase(SimpleTestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.middleware = PathBasedCsrfViewMiddleware(lambda r: HttpResponse())

    @override_settings(CSRF_REQUIRED_PATHS=None)
    def test_default_apply_everywhere(self):
        request = self.request_factory.get('/test')
        self.middleware.process_view(
            request,
            self.middleware.get_response,
            [],
            {}
        )
        self.assertTrue(hasattr(request, "csrf_processing_done"))

    @override_settings(CSRF_REQUIRED_PATHS=("/admin", ))
    def test_do_not_apply_to_path(self):
        request = self.request_factory.get('/test')
        self.middleware.process_view(
            request,
            self.middleware.get_response,
            [],
            {}
        )
        self.assertFalse(hasattr(request, "csrf_processing_done"))

    @override_settings(CSRF_REQUIRED_PATHS=("/admin", ))
    def test_apply_to_path(self):
        request = self.request_factory.get('/admin')
        self.middleware.process_view(
            request,
            self.middleware.get_response,
            [],
            {}
        )
        self.assertTrue(hasattr(request, "csrf_processing_done"))
