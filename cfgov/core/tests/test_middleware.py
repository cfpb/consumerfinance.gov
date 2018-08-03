from django.test import TestCase, override_settings

import mock

from core.middleware import parse_links, should_parse_links


class TestParseLinksMiddleware(TestCase):
    @mock.patch('core.middleware.parse_links')
    def test_parse_links_gets_called(self, mock_parse_links):
        """Middleware correctly invokes parse links when rendering webpage"""
        response = self.client.get('/foo/bar')
        mock_parse_links.assert_called_with(response.content)

    @override_settings(PARSE_LINKS_BLACKLIST=['/foo/'])
    @mock.patch('core.middleware.parse_links')
    def test_parse_links_does_not_get_called_blacklist(self, mock_parse_links):
        """Middleware does not invoke parse links when path is in blacklist"""
        self.client.get('/foo/bar')
        mock_parse_links.assert_not_called()


class TestShouldParseLinks(TestCase):
    def test_should_not_parse_links_if_non_html(self):
        self.assertFalse(should_parse_links(
            request_path='/foo/bar',
            content_type='application/json'
        ))

    def test_should_parse_links_if_html(self):
        self.assertTrue(should_parse_links(
            request_path='/foo/bar',
            content_type='text/html'
        ))


class TestParseLinks(TestCase):
    def test_relative_link_remains_unmodified(self):
        self.assertEqual(
            parse_links('<a href="/something">text</a>'),
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
