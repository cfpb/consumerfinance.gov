from django.core.exceptions import ValidationError
from django.test import Client, TestCase

from wagtail.wagtailcore.blocks import StreamValue

from scripts import _atomic_helpers as atomic

from v1.atomic_elements.molecules import RSSFeed, TextIntroduction
from v1.models.browse_filterable_page import BrowseFilterablePage
from v1.models.browse_page import BrowsePage
from v1.models.landing_page import LandingPage
from v1.models.learn_page import DocumentDetailPage, LearnPage
from v1.models.sublanding_filterable_page import SublandingFilterablePage
from v1.models.sublanding_page import SublandingPage
from v1.tests.wagtail_pages.helpers import publish_page, save_new_page


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

    def test_notification(self):
        """Notification correctly displays on a Sublanding Page"""
        sublanding_page = SublandingPage(
            title='Sublanding Page',
            slug='sublanding',
        )
        sublanding_page.content = StreamValue(
            sublanding_page.content.stream_block,
            [atomic.notification],
            True
        )
        publish_page(child=sublanding_page)
        response = django_client.get('/sublanding/')
        self.assertContains(response, 'this is a notification message')
        self.assertContains(response, 'this is a notification explanation')
        self.assertContains(response, 'this is a notification link')

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


class TestTextIntroductionValidation(TestCase):

    def test_text_intro_without_eyebrow_or_heading_passes_validation(self):
        block = TextIntroduction()
        value = block.to_python({})

        try:
            block.clean(value)
        except ValidationError:
            self.fail('no heading and no eyebrow should not fail validation')

    def test_text_intro_with_just_heading_passes_validation(self):
        block = TextIntroduction()
        value = block.to_python({'heading': 'Heading'})

        try:
            block.clean(value)
        except ValidationError:
            self.fail('heading without eyebrow should not fail validation')

    def test_text_intro_with_eyebrow_but_no_heading_fails_validation(self):
        block = TextIntroduction()
        value = block.to_python({'eyebrow': 'Eyebrow'})

        with self.assertRaises(ValidationError):
            block.clean(value)

    def test_text_intro_with_heading_and_eyebrow_passes_validation(self):
        block = TextIntroduction()
        value = block.to_python({
            'heading': 'Heading',
            'eyebrow': 'Eyebrow'
        })

        try:
            block.clean(value)
        except ValidationError:
            self.fail('eyebrow with heading should not fail validation')


class RSSFeedTests(TestCase):
    def render(self, context):
        block = RSSFeed()

        # RSSFeed doesn't take any options.
        value = block.to_python({})

        return block.render(value=value, context=context)

    def assertHTMLContainsLinkToPageFeed(self, html, page):
        feed = page.url + 'feed/'
        self.assertIn('<a class="a-btn" href="{}">'.format(feed), html)

    def test_render_no_page_in_context_renders_nothing(self):
        html = self.render(context={})
        self.assertFalse(html.strip())

    def test_render_page_doesnt_provide_feed_renders_nothing(self):
        page = BrowsePage(title='test', slug='test')
        save_new_page(page)

        html = self.render(context={'page': page})
        self.assertFalse(html.strip())

    def test_render_page_provides_feed(self):
        page = SublandingFilterablePage(title='test', slug='test')
        save_new_page(page)

        html = self.render(context={'page': page})
        self.assertHTMLContainsLinkToPageFeed(html, page)

    def test_render_parent_page_provides_feed(self):
        parent_page = SublandingFilterablePage(title='test', slug='test')
        save_new_page(parent_page)

        child_page = BrowsePage(title='test', slug='test')
        save_new_page(child_page, root=parent_page)

        html = self.render(context={'page': child_page})
        self.assertHTMLContainsLinkToPageFeed(html, parent_page)

    def test_render_both_child_and_parent_page_provide_feed(self):
        parent_page = SublandingFilterablePage(title='test', slug='test')
        save_new_page(parent_page)

        child_page = SublandingFilterablePage(title='test', slug='test')
        save_new_page(child_page, root=parent_page)

        html = self.render(context={'page': child_page})
        self.assertHTMLContainsLinkToPageFeed(html, child_page)
