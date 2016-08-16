from django.test import TestCase
from v1 import parse_links, get_protected_url
# from bs4 import BeautifulSoup

import mock


class ImportDataTest(TestCase):

    def test_external_link(self):
        link = '<a href="https://wwww.google.com">external link/a>'
        output = str(parse_links(link))
        self.assertIn('external-site', output)
        self.assertIn('class="icon-link_text"', output)

    def test_cfpb_link(self):
        link = '<a href="http://www.consumerfinance.gov/foo">cfpb link</a>'
        output = str(parse_links(link))
        self.assertNotIn('external-site', output)
        self.assertNotIn('class="icon-link_text"', output)

    def test_gov_link(self):
        link = '<a href="http://www.fdic.gov/bar">gov link</a>'
        output = str(parse_links(link))
        self.assertNotIn('external-site', output)
        self.assertIn('class="icon-link_text"', output)


class LinkTest(TestCase):

    def setUp(self):

        self.page = mock.MagicMock()
        self.request = mock.MagicMock()
        self.request.url = 'http://localhost:8000/about-us/blog/'
        self.page.url = 'http://localhost:8000/about-us/blog/we-want-hear-public-about-payday-loans/'
        self.page.live = True
        self.page.specific.shared = True
        self.context = mock.MagicMock()

        def context_dict(name):
            return {'request': self.request}[name]

        self.context.__getitem__.side_effect = context_dict

    def test_get_protected_url(self):

        result = get_protected_url(self.context, None)
        self.assertEqual(result, '#')
        self.page.url = None
        result = get_protected_url(self.context, self.page)
        self.assertIs(result, None)
        self.page.url = 'http://localhost:8000/about-us/blog/we-want-hear-public-about-payday-loans/'
        result = get_protected_url(self.context, self.page)
        self.assertEqual(result, self.page.url)
        self.page.live = False
        result = get_protected_url(self.context, self.page)
        self.assertEqual(result, '#')
        self.request.url = 'http://content.localhost:8000/about-us/blog/'
        result = get_protected_url(self.context, self.page)
        self.assertEqual(result, 'http://content.localhost:8000/about-us/blog/we-want-hear-public-about-payday-loans/')


if __name__ == '__main__':
    unittest.main()

