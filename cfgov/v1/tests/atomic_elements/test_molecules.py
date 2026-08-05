import datetime
from io import StringIO

from django.template import engines
from django.test import SimpleTestCase, TestCase

from wagtail.blocks import StreamValue
from wagtail.blocks.struct_block import StructBlockValidationError
from wagtail.test.utils.wagtail_tests import WagtailTestUtils

from scripts import _atomic_helpers as atomic
from search.elasticsearch_helpers import ElasticsearchTestsMixin
from v1.atomic_elements.molecules import (
    ContactEmail,
    ContactHyperlink,
    RSSFeed,
    TextIntroduction,
)
from v1.documents import FilterablePagesDocument
from v1.models.browse_filterable_page import BrowseFilterablePage
from v1.models.browse_page import BrowsePage
from v1.models.landing_page import LandingPage
from v1.models.learn_page import DocumentDetailPage, LearnPage
from v1.models.sublanding_filterable_page import SublandingFilterablePage
from v1.models.sublanding_page import SublandingPage
from v1.tests.wagtail_pages.helpers import publish_page, save_new_page


class MoleculesTestCase(ElasticsearchTestsMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a clean index for the test suite
        cls.rebuild_elasticsearch_index(
            FilterablePagesDocument.Index.name, stdout=StringIO()
        )

    def test_text_intro(self):
        """Text introduction value correctly displays on a BFP"""
        bfp = BrowseFilterablePage(
            title="Browse Filterable Page",
            slug="browse-filterable-page",
        )
        bfp.header = StreamValue(
            bfp.header.stream_block, [atomic.text_introduction], True
        )
        publish_page(child=bfp)
        response = self.client.get("/browse-filterable-page/")
        self.assertContains(response, "this is an intro")

    def test_content_with_anchor(self):
        """Content with anchor value correctly displays on a Learn Page"""
        learn_page = LearnPage(title="Learn", slug="learn")
        learn_page.content = StreamValue(
            learn_page.content.stream_block, [atomic.full_width_text], True
        )
        publish_page(child=learn_page)
        response = self.client.get("/learn/")
        self.assertContains(response, "full width text block")
        self.assertContains(response, "this is an anchor link")

    def test_quote(self):
        """Quote value correctly displays on a Learn Page"""
        learn_page = LearnPage(title="Learn", slug="learn")
        learn_page.content = StreamValue(
            learn_page.content.stream_block, [atomic.full_width_text], True
        )
        publish_page(child=learn_page)
        response = self.client.get("/learn/")
        self.assertContains(response, "this is a quote")
        self.assertContains(response, "a citation")

    def test_call_to_action(self):
        """Call to action value correctly displays on a Learn Page"""
        learn_page = LearnPage(
            title="Learn",
            slug="learn",
        )
        learn_page.content = StreamValue(
            learn_page.content.stream_block, [atomic.call_to_action], True
        )
        publish_page(child=learn_page)
        response = self.client.get("/learn/")
        self.assertContains(response, "this is a call to action")

    def test_notification(self):
        """Notification correctly displays on a Sublanding Page"""
        sublanding_page = SublandingPage(
            title="Sublanding Page",
            slug="sublanding",
        )
        sublanding_page.content = StreamValue(
            sublanding_page.content.stream_block, [atomic.notification], True
        )
        publish_page(child=sublanding_page)
        response = self.client.get("/sublanding/")
        self.assertContains(response, "this is a notification message")
        self.assertContains(response, "this is a notification explanation")
        self.assertContains(response, "this is a notification link")

    def test_hero(self):
        """Hero heading correctly displays on a Sublanding Filterable Page"""
        sfp = SublandingFilterablePage(
            title="Sublanding Filterable Page",
            slug="sfp",
        )
        sfp.header = StreamValue(sfp.header.stream_block, [atomic.hero], True)
        publish_page(child=sfp)
        response = self.client.get("/sfp/")
        self.assertContains(response, "this is a hero heading")

    def test_related_links(self):
        """Related links value correctly displays on a Landing Page"""
        landing_page = LandingPage(
            title="Landing Page",
            slug="landing",
        )
        landing_page.sidefoot = StreamValue(
            landing_page.sidefoot.stream_block, [atomic.related_links], True
        )
        publish_page(child=landing_page)
        response = self.client.get("/landing/")
        self.assertContains(response, "this is a related link")

    def test_expandable(self):
        """Expandable label value correctly displays on a Browse Page"""
        browse_page = BrowsePage(
            title="Browse Page",
            slug="browse",
        )
        browse_page.content = StreamValue(
            browse_page.content.stream_block,
            [atomic.expandable],
            True,
        )
        publish_page(child=browse_page)
        response = self.client.get("/browse/")
        self.assertContains(response, "this is an expandable")

    def test_related_metadata(self):
        """Related metadata heading correctly displays on a DDP"""
        ddp = DocumentDetailPage(
            title="Document Detail Page",
            slug="ddp",
        )
        ddp.sidefoot = StreamValue(
            ddp.sidefoot.stream_block,
            [atomic.related_metadata],
            True,
        )
        publish_page(child=ddp)
        response = self.client.get("/ddp/")
        self.assertContains(response, "this is a related metadata heading")


class ContactEmailTests(SimpleTestCase):
    def test_clean_email_required(self):
        block = ContactEmail()
        value = block.to_python({"emails": []})
        with self.assertRaises(StructBlockValidationError):
            block.clean(value)

    def test_clean_valid(self):
        block = ContactEmail()
        value = block.to_python({"emails": [{"url": "foo@example.com"}]})
        self.assertTrue(block.clean(value))

    def test_render_no_link_text(self):
        block = ContactEmail()
        value = block.to_python({"emails": [{"url": "foo@example.com"}]})
        self.assertInHTML(
            '<a href="mailto:foo@example.com">foo@example.com</a>',
            block.render(value),
        )

    def test_render_with_link_text(self):
        block = ContactEmail()
        value = block.to_python(
            {
                "emails": [
                    {
                        "url": "foo@example.com",
                        "text": "Bar",
                    },
                ],
            }
        )

        self.assertInHTML(
            '<a href="mailto:foo@example.com">Bar</a>', block.render(value)
        )


class ContactHyperlinkTests(SimpleTestCase):
    def test_render_no_link_text(self):
        block = ContactHyperlink()
        value = block.to_python({"url": "https://example.com"})
        self.assertInHTML(
            '<a href="https://example.com">https://example.com</a>',
            block.render(value),
        )

    def test_render_with_link_text(self):
        block = ContactHyperlink()
        value = block.to_python(
            {
                "url": "https://example.com",
                "text": "Example",
            }
        )
        self.assertInHTML(
            '<a href="https://example.com">Example</a>', block.render(value)
        )


class TestTextIntroductionValidation(TestCase):
    def test_text_intro_without_eyebrow_or_heading_passes_validation(self):
        block = TextIntroduction()
        value = block.to_python({})

        try:
            block.clean(value)
        except StructBlockValidationError:  # pragma: no cover
            self.fail("no heading and no eyebrow should not fail validation")

    def test_text_intro_with_just_heading_passes_validation(self):
        block = TextIntroduction()
        value = block.to_python({"heading": "Heading"})

        try:
            block.clean(value)
        except StructBlockValidationError:  # pragma: no cover
            self.fail("heading without eyebrow should not fail validation")

    def test_text_intro_with_eyebrow_but_no_heading_fails_validation(self):
        block = TextIntroduction()
        value = block.to_python({"eyebrow": "Eyebrow"})

        with self.assertRaises(StructBlockValidationError):
            block.clean(value)

    def test_text_intro_with_heading_and_eyebrow_passes_validation(self):
        block = TextIntroduction()
        value = block.to_python({"heading": "Heading", "eyebrow": "Eyebrow"})

        try:
            block.clean(value)
        except StructBlockValidationError:  # pragma: no cover
            self.fail("eyebrow with heading should not fail validation")


class RSSFeedTests(TestCase):
    def render(self, context):
        block = RSSFeed()

        # RSSFeed doesn't take any options.
        value = block.to_python({})

        return block.render(value=value, context=context)

    def assertHTMLContainsLinkToPageFeed(self, html, page):
        feed = page.url + "feed/"
        self.assertIn(f'<a class="a-btn" href="{feed}">', html)

    def test_render_no_page_in_context_renders_nothing(self):
        html = self.render(context={})
        self.assertFalse(html.strip())

    def test_render_page_doesnt_provide_feed_renders_nothing(self):
        page = BrowsePage(title="test", slug="test")
        save_new_page(page)

        html = self.render(context={"page": page})
        self.assertFalse(html.strip())

    def test_render_page_provides_feed(self):
        page = SublandingFilterablePage(title="test", slug="test")
        save_new_page(page)

        html = self.render(context={"page": page})
        self.assertHTMLContainsLinkToPageFeed(html, page)

    def test_render_parent_page_provides_feed(self):
        parent_page = SublandingFilterablePage(title="test", slug="test")
        save_new_page(parent_page)

        child_page = BrowsePage(title="test", slug="test")
        save_new_page(child_page, root=parent_page)

        html = self.render(context={"page": child_page})
        self.assertHTMLContainsLinkToPageFeed(html, parent_page)

    def test_render_both_child_and_parent_page_provide_feed(self):
        parent_page = SublandingFilterablePage(title="test", slug="test")
        save_new_page(parent_page)

        child_page = SublandingFilterablePage(title="test", slug="test")
        save_new_page(child_page, root=parent_page)

        html = self.render(context={"page": child_page})
        self.assertHTMLContainsLinkToPageFeed(html, child_page)


class PaginationTests(WagtailTestUtils, SimpleTestCase):
    def setUp(self):
        self.jinja_engine = engines["wagtail-env"]
        self.template_source = """
{% import "v1/includes/molecules/pagination.html" as pagination %}
{{ pagination.render(
    total_pages, current_page, fragment_id, index, extra_params
) }}
""".strip()

    def render(self, **kwargs):
        template = self.jinja_engine.from_string(self.template_source)
        return template.render(kwargs)

    def test_no_output_when_only_one_page(self):
        html = self.render(total_pages=1, current_page=1)
        self.assertEqual(html.strip(), "")

    def test_no_output_when_current_page_beyond_total(self):
        html = self.render(total_pages=3, current_page=4)
        self.assertEqual(html.strip(), "")

    def test_middle_page_has_both_prev_and_next_links(self):
        html = self.render(total_pages=3, current_page=2)
        self.assertTagInHTML(
            '<a class="a-btn m-pagination__btn-prev" href="?page=1">', html
        )
        self.assertTagInHTML(
            '<a class="a-btn m-pagination__btn-next" href="?page=3">', html
        )

    def test_first_page_disables_prev_link(self):
        html = self.render(total_pages=3, current_page=1)
        self.assertTagInHTML(
            '<a class="a-btn a-btn--disabled m-pagination__btn-prev">', html
        )
        self.assertTagInHTML(
            '<a class="a-btn m-pagination__btn-next" href="?page=2">', html
        )

    def test_last_page_disables_next_link(self):
        html = self.render(total_pages=3, current_page=3)
        self.assertTagInHTML(
            '<a class="a-btn m-pagination__btn-prev" href="?page=2">', html
        )
        self.assertTagInHTML(
            '<a class="a-btn a-btn--disabled m-pagination__btn-next">', html
        )

    def test_fragment_id_appended_to_links(self):
        html = self.render(
            total_pages=3, current_page=2, fragment_id="my-results"
        )
        self.assertIn('href="?page=1#my-results">', html)
        self.assertIn('href="?page=3#my-results">', html)

    def test_index_used_in_current_page_field_id(self):
        html = self.render(total_pages=3, current_page=2, index=7)
        self.assertIn('id="m-pagination__current-page-7"', html)

    def test_string_extra_param_included_in_links_and_hidden_field(self):
        html = self.render(
            total_pages=3, current_page=2, extra_params={"q": "hello world"}
        )
        self.assertIn('href="?page=1&q=hello world">', html)
        self.assertIn('href="?page=3&q=hello world">', html)
        self.assertTagInHTML(
            '<input type="hidden" name="q" value="hello world">', html
        )

    def test_list_extra_param_repeated_for_each_value(self):
        html = self.render(
            total_pages=3,
            current_page=2,
            extra_params={"categories": ["a", "b"]},
        )
        self.assertIn('href="?page=1&categories=a&categories=b">', html)
        self.assertTagInHTML(
            '<input type="hidden" name="categories" value="a">', html
        )
        self.assertTagInHTML(
            '<input type="hidden" name="categories" value="b">', html
        )

    def test_empty_list_extra_param_produces_nothing(self):
        html = self.render(
            total_pages=3, current_page=2, extra_params={"categories": []}
        )
        self.assertNotIn("categories", html)

    def test_non_string_scalar_extra_param_is_stringified(self):
        html = self.render(
            total_pages=3, current_page=2, extra_params={"results": 50}
        )
        self.assertIn("results=50", html)

    def test_date_extra_param_is_stringified(self):
        html = self.render(
            total_pages=3,
            current_page=2,
            extra_params={"from_date": datetime.date(2024, 1, 15)},
        )
        self.assertIn("from_date=2024-01-15", html)

    def test_none_and_empty_string_extra_params_are_omitted(self):
        html = self.render(
            total_pages=3,
            current_page=2,
            extra_params={"from_date": None, "title": ""},
        )
        self.assertNotIn("from_date", html)
        self.assertNotIn("title", html)

    def test_page_and_partial_keys_are_always_excluded(self):
        html = self.render(
            total_pages=3,
            current_page=2,
            extra_params={"page": 99, "partial": True, "q": "hi"},
        )
        self.assertNotIn("page=99", html)
        self.assertNotIn("partial", html)
        self.assertIn("q=hi", html)

    def test_extra_param_values_are_html_escaped(self):
        html = self.render(
            total_pages=3,
            current_page=2,
            extra_params={"q": '"><script>alert(1)</script>'},
        )
        self.assertNotIn("<script>", html)
        self.assertIn("&#34;&gt;&lt;script&gt;alert(1)&lt;/script&gt;", html)
