from django.test import TestCase

from wagtail.wagtailcore.models import Page, Site

from v1.routing import get_url_parts_for_site
from v1.tests.wagtail_pages.helpers import save_new_page


class GetUrlPartsForSiteTestCase(TestCase):
    def setUp(self):
        self.root = Page.objects.get(slug='cfgov')
        self.www = Site.objects.get(hostname='localhost')

    def test_get_root_from_www(self):
        self.assertEqual(
            get_url_parts_for_site(self.root, self.www),
            (self.www.id, self.www.root_url, '/')
        )

    def test_get_page_from_www(self):
        new_page = Page(title='test', slug='foo')
        save_new_page(new_page, root=self.root)

        self.assertEqual(
            get_url_parts_for_site(new_page, self.www),
            (self.www.id, self.www.root_url, '/foo/')
        )

    def test_page_not_routable_on_site_returns_none(self):
        new_page = Page(title='test', slug='foo')
        save_new_page(new_page, root=self.root)

        new_site = Site.objects.create(hostname='test', root_page=new_page)
        self.assertIsNone(get_url_parts_for_site(self.root, new_site))
