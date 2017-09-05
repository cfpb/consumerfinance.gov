from django.test import Client, TestCase
from wagtail.wagtailcore.blocks import StreamValue

from scripts import _atomic_helpers as atomic
from v1.atomic_elements.molecules import FormFieldWithButton
from v1.models.browse_filterable_page import BrowseFilterablePage
from v1.models.browse_page import BrowsePage
from v1.models.landing_page import LandingPage
from v1.models.learn_page import DocumentDetailPage, LearnPage
from v1.models.sublanding_filterable_page import SublandingFilterablePage
from v1.models.sublanding_page import SublandingPage
from v1.tests.wagtail_pages.helpers import publish_page

django_client = Client()


class MoleculesTestCase(TestCase):

    def test_text_intro(self):
        """Text introduction value correctly displays on a Browse Filterable Page"""
        bfp = BrowseFilterablePage(
            title='Browse Filterable Page',
            slug='browse-filterable-page',
        )
        bfp.header = StreamValue(
            bfp.header.stream_block,
            [atomic.text_introduction],
            True
        )
        publish_page(child=bfp)
        response = django_client.get('/browse-filterable-page/')
        self.assertContains(response, 'this is an intro')

    def test_featured_content(self):
        """Featured content value correctly displays on a Browse Page"""
        bp = BrowsePage(
            title='Browse Page',
            slug='browse-page',
        )
        bp.header = StreamValue(bp.header.stream_block,
        [
            atomic.featured_content
        ], True)
        bp.content = StreamValue(bp.content.stream_block,
        [
            atomic.expandable,
            atomic.expandable_group
        ], True)
        publish_page(child=bp)
        response = django_client.get('/browse-page/')
        self.assertContains(response, 'this is a featured content body')

    def test_content_with_anchor(self):
        """Content with anchor value correctly displays on a Learn Page"""
        learn_page = LearnPage(
            title='Learn',
            slug='learn'
        )
        learn_page.content = StreamValue(
            learn_page.content.stream_block,
            [atomic.full_width_text],
            True
        )
        publish_page(child=learn_page)
        response = django_client.get('/learn/')
        self.assertContains(response, 'full width text block')
        self.assertContains(response, 'this is an anchor link')

    def test_quote(self):
        """Quote value correctly displays on a Learn Page"""
        learn_page = LearnPage(
            title='Learn',
            slug='learn'
        )
        learn_page.content = StreamValue(
            learn_page.content.stream_block,
            [atomic.full_width_text],
            True
        )
        publish_page(child=learn_page)
        response = django_client.get('/learn/')
        self.assertContains(response, 'this is a quote')
        self.assertContains(response, 'a citation')

    def test_call_to_action(self):
        """Call to action value correctly displays on a Learn Page"""
        learn_page = LearnPage(
            title='Learn',
            slug='learn',
        )
        learn_page.content = StreamValue(
            learn_page.content.stream_block,
            [atomic.call_to_action],
            True
        )
        publish_page(child=learn_page)
        response = django_client.get('/learn/')
        self.assertContains(response, 'this is a call to action')

    def test_hero(self):
        """Hero heading correctly displays on a Sublanding Filterable Page"""
        sfp = SublandingFilterablePage(
            title='Sublanding Filterable Page',
            slug='sfp',
        )
        sfp.header = StreamValue(
            sfp.header.stream_block,
            [atomic.hero],
            True
        )
        publish_page(child=sfp)
        response = django_client.get('/sfp/')
        self.assertContains(response, 'this is a hero heading')


    def test_related_links(self):
        """Related links value correctly displays on a Landing Page"""
        landing_page = LandingPage(
            title='Landing Page',
            slug='landing',
        )
        landing_page.sidefoot = StreamValue(
            landing_page.sidefoot.stream_block,
            [atomic.related_links],
            True
        )
        publish_page(child=landing_page)
        response = django_client.get('/landing/')
        self.assertContains(response, 'this is a related link')

    def test_half_width_link_blob(self):
        """Half width link blob value correctly displays on a Landing Page"""
        landing_page = LandingPage(
            title='Landing Page',
            slug='landing',
        )
        landing_page.content = StreamValue(
            landing_page.content.stream_block,
            [atomic.half_width_link_blob_group],
            True
        )
        publish_page(child=landing_page)
        response = django_client.get('/landing/')
        self.assertContains(response, 'this is a half width link blob')

    def test_rss_feed(self):
        """RSS feed correctly displays on a Sublanding Page"""
        sublanding_page = SublandingPage(
            title='Sublanding Page',
            slug='sublanding',
        )
        sublanding_page.sidefoot = StreamValue(
            sublanding_page.sidefoot.stream_block,
            [atomic.rss_feed],
            True
        )
        publish_page(sublanding_page)
        response = django_client.get('/sublanding/')
        self.assertContains(response, 'rss-subscribe-section')

    def test_expandable(self):
        """Expandable label value correctly displays on a Browse Page"""
        browse_page = BrowsePage(
            title='Browse Page',
            slug='browse',
        )
        browse_page.content = StreamValue(
            browse_page.content.stream_block,
            [atomic.expandable],
            True,
        )
        publish_page(child=browse_page)
        response = django_client.get('/browse/')
        self.assertContains(response, 'this is an expandable')

    def test_related_metadata(self):
        """Related metadata heading correctly displays on a Document Detail Page"""
        ddp = DocumentDetailPage(
            title='Document Detail Page',
            slug='ddp',
        )
        ddp.sidefoot = StreamValue(
            ddp.sidefoot.stream_block,
            [atomic.related_metadata],
            True,
        )
        publish_page(child=ddp)
        response = django_client.get('/ddp/')
        self.assertContains(response, 'this is a related metadata heading')

    def test_image_texts(self):
        """Image Text molecules correctly display on a Landing Page"""
        landing_page = LandingPage(
            title='Landing Page',
            slug='landing',
        )
        landing_page.content = StreamValue(
            landing_page.content.stream_block,
            [
                atomic.image_text_50_50_group,
                atomic.image_text_25_75_group
            ],
            True,
        )
        publish_page(child=landing_page)
        response = django_client.get('/landing/')
        self.assertContains(response, 'this is an image text in a 50 50 group')
        self.assertContains(response, 'this is an image text in a 25 75 group')

    def test_formfield_with_button(self):
        """FormField with Button correctly displays on a Sublanding Page"""
        sublanding_page = DocumentDetailPage(
            title='Sublanding Page',
            slug='sublanding',
        )
        sublanding_page.sidefoot = StreamValue(
            sublanding_page.sidefoot.stream_block,
            [atomic.email_signup],
            True,
        )
        publish_page(child=sublanding_page)
        response = django_client.get('/sublanding/')
        self.assertContains(response, 'this is a form field with button')
        self.assertNotContains(response, '(required)')
