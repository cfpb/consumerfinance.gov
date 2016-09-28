from django.test import TestCase
from v1 import parse_links, get_protected_url

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
    """
    The get_protected_url function is a template tag that is applied to links to make sure
    that the returned URL is something that is allowed to be accessed by the user. Under some
    conditions, get_protected_url returns the hash mark '#' which results in a non-navigable URL.
    """

    def setUp(self):

        self.page = mock.MagicMock()
        self.request = mock.MagicMock()
        self.request.url = 'http://localhost:8000/path/to/page/'
        self.page.url = 'http://localhost:8000/path/to/some/other/page/'
        self.page.live = True
        self.page.specific.shared = True
        self.context = mock.MagicMock()

        def context_dict(name):
            return {'request': self.request}[name]

        self.context.__getitem__.side_effect = context_dict

    def test_get_protected_url_no_page(self):
        """
        Confirm that in the absence of a page, get_protected_url returns the hash.
        """
        result = get_protected_url(self.context, None)
        self.assertEqual(result, '#')

    def test_get_protected_url_no_url(self):
        """
        Confirm that in the absence of a page URL, get_protected_url returns None.
        """
        self.page.url = None
        result = get_protected_url(self.context, self.page)
        self.assertIsNone(result)

    def test_get_protected_url_live_page(self):
        """
        Confirm that if a live page is requested from the same host as the request
        we get back the original page url.
        """
        self.page.url = 'http://localhost:8000/path/to/some/other/page/'
        result = get_protected_url(self.context, self.page)
        self.assertEqual(result, self.page.url)

    def test_get_protected_url_non_live_page(self):
        """
        Confirm that if a non-live page is requested from a live page, we get back the hash.
        """
        self.page.live = False
        result = get_protected_url(self.context, self.page)
        self.assertEqual(result, '#')

    def test_get_protected_url_staging(self):
        """
        Make sure that if we're on the staging site and request a page from that site
        which does not point to the same host, that we replace the hostname with the
        staging hostname.
        """
        self.page.live = False
        self.request.url = 'http://content.localhost:8000/path/to/page/'
        self.page.url = 'http://localhost:8000/path/to/some/other/page/'
        result = get_protected_url(self.context, self.page)
        self.assertEqual(result, 'http://content.localhost:8000/path/to/some/other/page/')


if __name__ == '__main__':
    unittest.main()

