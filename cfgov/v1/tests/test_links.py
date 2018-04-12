from django.http import HttpRequest
from django.template import engines
from django.template.response import TemplateResponse
from django.test import TestCase

from wagtail.wagtailcore.models import Site

from bs4 import BeautifulSoup

from v1 import get_protected_url, parse_links
from v1.models import CFGOVPage
from v1.tests.wagtail_pages.helpers import save_new_page


class ParseLinksTests(TestCase):
    def test_parse_links_returns_beautiful_soup(self):
        self.assertIsInstance(
            parse_links('<a href="/something">text</a>'),
            BeautifulSoup
        )

    def test_external_link(self):
        link = '<a href="https://wwww.google.com">external link/a>'
        output = str(parse_links(link))
        self.assertIn('external-site', output)
        self.assertIn('cf-icon-external-link', output)

    def test_cfpb_link(self):
        link = '<a href="https://www.consumerfinance.gov/foo">cfpb link</a>'
        output = str(parse_links(link))
        self.assertNotIn('external-site', output)
        self.assertNotIn('cf-icon-external-link', output)

    def test_gov_link(self):
        link = '<a href="https://www.fdic.gov/bar">gov link</a>'
        output = str(parse_links(link))
        self.assertNotIn('external-site', output)
        self.assertIn('cf-icon-external-link', output)

    def test_pdf_link_gets_download_icon(self):
        link = '<a href="/something.pdf">link</a>'
        parsed = str(parse_links(link))
        self.assertIn('cf-icon-download', parsed)

    def test_different_case_pdf_link_gets_download_icon(self):
        link = '<a href="/something.PDF">link</a>'
        parsed = str(parse_links(link))
        self.assertIn('cf-icon-download', parsed)


class GetProtectedUrlTestCase(TestCase):
    def test_get_live_page_from_www_returns_relative_url(self):
        page = self.make_page(path='foo', live=True)
        context = {'request': self.request_for_hostname('localhost')}
        protected_url = get_protected_url(context, page)
        self.assertEquals(protected_url, '/foo/')

    def test_get_draft_page_from_www_returns_hash(self):
        page = self.make_page(path='foo', live=False)
        context = {'request': self.request_for_hostname('localhost')}
        protected_url = get_protected_url(context, page)
        self.assertEquals(protected_url, '#')

    def test_get_null_page_from_www_returns_hash(self):
        context = {'request': self.request_for_hostname('localhost')}
        protected_url = get_protected_url(context, None)
        self.assertEquals(protected_url, '#')

    def test_context_without_request_raises_keyerror(self):
        page = self.make_page(path='foo', live=True)
        context = {}

        with self.assertRaises(KeyError):
            get_protected_url(context, page)

    def test_render_page(self):
        template_string = 'url: {{ get_protected_url(page) }}'
        template = engines['wagtail-env'].from_string(template_string)

        page = self.make_page(path='foo', live=True)
        request = self.request_for_hostname('localhost')
        context = page.get_context(request)

        response = TemplateResponse(request, template, context)
        response.render()

        self.assertEqual(response.content, 'url: /foo/')

    def make_page(self, path, live):
        page = CFGOVPage(slug=path, title=path)
        page.live = live
        save_new_page(page)
        return page

    def request_for_hostname(self, hostname):
        request = HttpRequest()
        request.META['SERVER_NAME'] = hostname
        request.site = Site.objects.get(hostname=hostname)
        return request
