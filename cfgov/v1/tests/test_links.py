from django.test import TestCase
from v1 import parse_links
from bs4 import BeautifulSoup

class ImportDataTest(TestCase):
    def test_external_link(self):
        soup = BeautifulSoup('<a href="https://wwww.google.com">external link/a>', 'html.parser')
        output = str(parse_links(soup))
        self.assertIn('external-site', output)
        self.assertIn('class="icon-link_text"', output)

    def test_cfpb_link(self):
        soup = BeautifulSoup('<a href="http://www.consumerfinance.gov/foo">cfpb link</a>', 'html.parser')
        output = str(parse_links(soup))
        self.assertNotIn('external-site', output)
        self.assertNotIn('class="icon-link_text"', output)

    def test_gov_link(self):
        soup = BeautifulSoup('<a href="http://www.fdic.gov/bar">gov link</a>', 'html.parser')
        output = str(parse_links(soup))
        self.assertNotIn('external-site', output)
        self.assertIn('class="icon-link_text"', output)


if __name__ == '__main__':
    unittest.main()

