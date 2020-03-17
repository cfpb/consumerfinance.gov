# -*- coding: utf-8 -*-

from django.test import TestCase, override_settings

import mock
from bs4 import BeautifulSoup

from core.middleware import ParseLinksMiddleware, parse_links
from v1.models import CFGOVPage
from v1.tests.wagtail_pages.helpers import publish_page


@mock.patch('core.middleware.parse_links')
class TestParseLinksMiddleware(TestCase):
    def test_parse_links_gets_called(self, mock_parse_links):
        """Middleware correctly invokes parse links when rendering webpage"""
        response = self.client.get('/foo/bar')
        mock_parse_links.assert_called_with(response.content, encoding='utf-8')

    @override_settings(PARSE_LINKS_EXCLUSION_LIST=[r'^/foo/'])
    def test_parse_links_does_not_get_called_excluded(self, mock_parse_links):
        """Middleware does not invoke parse links when path is excluded"""
        self.client.get('/foo/bar')
        mock_parse_links.assert_not_called()


class TestShouldParseLinks(TestCase):
    def test_should_not_parse_links_if_non_html(self):
        self.assertFalse(ParseLinksMiddleware.should_parse_links(
            request_path='/foo/bar',
            response_content_type='application/json'
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
            parse_links('<a href="/something">text</a>'),
            '<a href="/something">text</a>'
        )

    def test_works_properly_on_bytestrings(self):
        self.assertEqual(
            parse_links(b'<a href="/something">text</a>'),
            '<a href="/something">text</a>'
        )

    def test_non_gov_link(self):
        """Non gov links get external link icon and redirect."""
        link = '<a href="https://wwww.google.com">external link</a>'
        output = parse_links(link)
        self.assertIn('external-site', output)
        self.assertIn('cf-icon-svg', output)

    def test_gov_link(self):
        """Gov links get external link icon but not redirect."""
        link = '<a href="https://www.fdic.gov/bar">gov link</a>'
        output = parse_links(link)
        self.assertIn('cf-icon-svg', output)

    def test_internal_link(self):
        """Internal links get neither icon nor redirect."""
        link = '<a href="https://www.consumerfinance.gov/foo">cfpb link</a>'
        output = parse_links(link)
        self.assertNotIn('external-site', output)
        self.assertNotIn('cf-icon-svg', output)

    def test_files_get_download_icon(self):
        file_types = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'csv', 'zip']
        for file_type in file_types:
            link = '<a href="/something.{}">link</a>'.format(file_type)
            output = parse_links(link)
            self.assertIn('cf-icon-svg', output)

    def test_different_case_pdf_link_gets_download_icon(self):
        link = '<a href="/something.PDF">link</a>'
        output = parse_links(link)
        self.assertIn('cf-icon-svg', output)

    def test_rich_text_links_get_expanded(self):
        page = CFGOVPage(title='foo bar', slug='foo-bar')
        publish_page(page)
        link = '<a id="{}" linktype="page">foo bar</a>'.format(page.id)
        output = parse_links(link)
        self.assertEqual('<a href="/foo-bar/">foo bar</a>', output)

    def test_non_default_encoding(self):
        s = '<a href="/something">哈哈</a>'
        encoding = 'gb2312'
        parsed = parse_links(s.encode(encoding), encoding=encoding)
        self.assertEqual(parsed, s)

    def test_external_link_with_attribute(self):
        s = '<a href="https://somewhere/foo" data-thing="something">Link</a>'
        output = parse_links(s)
        self.assertIn('external-site', output)
        self.assertIn('cf-icon-svg', output)

    def test_external_link_with_img(self):
        s = '<a href="https://somewhere/foo"><img src="some.png"></a>'
        output = parse_links(s)
        self.assertIn('external-site', output)
        self.assertNotIn('cf-icon-svg', output)

    def test_external_link_with_background_img(self):
        s = ('<a href="https://somewhere/foo"><span>'
             '<div style="background-image: url(\'some.png\')"></div>'
             '</span></a>')
        output = parse_links(s)
        self.assertIn('external-site', output)
        self.assertNotIn('cf-icon-svg', output)

    def test_external_link_with_header(self):
        s = '<a href="https://somewhere/foo"><h3>Header</h3></a>'
        output = parse_links(s)
        self.assertIn('external-site', output)
        self.assertNotIn('cf-icon-svg', output)

    def test_multiline_external_gov_link(self):
        s = '''<a class="m-list_link a-link"
        href="https://usa.gov/">
        <span>
        USA
        .gov</span>
        </a>
        '''
        output = parse_links(s)
        self.assertIn('cf-icon-svg', output)

    def test_multiple_links(self):
        s = ('<a href="https://first.com">one</a>'
             '<a href="https://second.com">two</a>')
        output = parse_links(s)
        soup = BeautifulSoup(output, 'html.parser')
        self.assertEqual(len(soup.find_all('a')), 2)

    def check_after_parse_links_has_this_many_svgs(self, count, s):
        output = parse_links(s)
        soup = BeautifulSoup(output, 'html.parser')
        self.assertEqual(len(soup.find_all('svg')), count)

    def test_link_ending_with_svg_doesnt_get_another_svg(self):
        self.check_after_parse_links_has_this_many_svgs(1, (
            '<a href="https://external.gov">'
            '<span>Text before icon</span> '
            '<svg>something</svg>'
            '</a>'
        ))

    def test_link_ending_with_svg_and_whitespace_doesnt_get_another_svg(self):
        self.check_after_parse_links_has_this_many_svgs(1, (
            '<a href="https://external.gov">'
            '<span>Text before icon</span> '
            '<svg>something</svg>   \n\t'
            '</a>'
        ))

    def test_with_svg_not_at_the_end_still_gets_svg(self):
        self.check_after_parse_links_has_this_many_svgs(2, (
            '<a href="https://external.gov">'
            '<span><svg>something</svg> Text after icon</span>'
            '</a>'
        ))

    def test_with_svg_then_span_still_gets_svg(self):
        self.check_after_parse_links_has_this_many_svgs(2, (
            '<a href="https://external.gov">'
            '<svg>something</svg>'
            '<span>Text after icon</span>'
            '</a>'
        ))
