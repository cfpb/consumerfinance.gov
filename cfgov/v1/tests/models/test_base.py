import json

from django.test import TestCase
from django.test.client import RequestFactory

from wagtail import blocks
from wagtail.models import Page, Site

from v1.models import (
    AbstractFilterPage,
    BrowsePage,
    CFGOVPage,
    LandingPage,
    SublandingPage,
)
from v1.models.banners import Banner
from v1.tests.wagtail_pages.helpers import save_new_page


class TestCFGOVPageContext(TestCase):
    def setUp(self):
        self.page = CFGOVPage(title="Test", slug="test")
        self.factory = RequestFactory()
        self.request = self.factory.get("/")

    def test_get_context_no_banners(self):
        test_context = self.page.get_context(self.request)
        self.assertFalse(test_context["banners"])

    def test_get_context_one_banner_not_matching(self):
        Banner.objects.create(title="Banner", url_pattern="foo", enabled=True)
        test_context = self.page.get_context(self.request)
        self.assertFalse(test_context["banners"])

    def test_get_context_one_banner_matching(self):
        Banner.objects.create(title="Banner", url_pattern="/", enabled=True)
        test_context = self.page.get_context(self.request)
        self.assertTrue(test_context["banners"])

    def test_get_context_one_banner_matching_disabled(self):
        Banner.objects.create(title="Banner", url_pattern="/", enabled=False)
        test_context = self.page.get_context(self.request)
        self.assertFalse(test_context["banners"])

    def test_get_context_multiple_banners_matching(self):
        Banner.objects.create(title="Banner", url_pattern="/", enabled=True)
        Banner.objects.create(title="Banner2", url_pattern="/", enabled=True)
        Banner.objects.create(title="Banner3", url_pattern="/", enabled=False)
        Banner.objects.create(title="Banner4", url_pattern="foo", enabled=True)
        test_context = self.page.get_context(self.request)
        self.assertEqual(test_context["banners"].count(), 2)

    def test_get_context_sets_meta_description_from_search_description(self):
        result = "Correct Meta Description"
        self.page = LandingPage(
            title="test",
            search_description=result,
            header=json.dumps(
                [
                    {
                        "type": "hero",
                        "value": {"body": "Incorrect Meta Description"},
                    }
                ]
            ),
        )
        test_context = self.page.get_context(self.request)
        self.assertEqual(test_context["meta_description"], result)

    def test_get_context_sets_meta_description_from_hero(self):
        expected = "Correct Meta Description"
        self.page = LandingPage(
            title="test",
            header=json.dumps(
                [
                    {
                        "type": "text_introduction",
                        "value": {"intro": "Incorrect Meta Description"},
                    },
                    {
                        "type": "hero",
                        "value": {"body": expected},
                    },
                ]
            ),
            content=json.dumps(
                [
                    {
                        "type": "text_introduction",
                        "value": {"intro": "Incorrect Meta Description"},
                    }
                ]
            ),
        )
        test_context = self.page.get_context(self.request)
        result = test_context["meta_description"]
        self.assertEqual(expected, result)

    def test_get_context_sets_meta_description_from_header_text_introduction_intro(  # noqa: E501
        self,
    ):
        expected = "Correct Meta Description"
        self.page = LandingPage(
            title="test",
            header=json.dumps(
                [
                    {
                        "type": "text_introduction",
                        "value": {"intro": expected},
                    },
                    {
                        "type": "text_introduction",
                        "value": {"intro": "Incorrect Meta Description"},
                    },
                ]
            ),
            content=json.dumps(
                [
                    {
                        "type": "text_introduction",
                        "value": {"intro": "Incorrect Meta Description"},
                    }
                ]
            ),
        )
        test_context = self.page.get_context(self.request)
        result = test_context["meta_description"]
        self.assertEqual(expected, result)

    def test_get_context_sets_meta_description_from_content_text_introduction_intro(  # noqa: E501
        self,
    ):
        expected = "Correct Meta Description"
        self.page = SublandingPage(
            title="test",
            header=json.dumps(
                [
                    {
                        "type": "text_introduction",
                        "value": {"body": "Incorrect Meta Description"},
                    },
                ]
            ),
            content=json.dumps(
                [{"type": "text_introduction", "value": {"intro": expected}}]
            ),
        )
        test_context = self.page.get_context(self.request)
        result = test_context["meta_description"]
        self.assertEqual(expected, result)

    def test_get_context_sets_meta_description_from_header_item_introduction_paragraph(  # noqa: E501
        self,
    ):
        expected = "Correct Meta Description"
        self.page = AbstractFilterPage(
            title="test",
            header=json.dumps(
                [
                    {
                        "type": "item_introduction",
                        "value": {"paragraph": expected},
                    },
                ]
            ),
        )
        test_context = self.page.get_context(self.request)
        result = test_context["meta_description"]
        self.assertEqual(expected, result)

    def test_get_context_sets_meta_description_to_blank_if_no_other_data_to_set(  # noqa: E501
        self,
    ):
        expected = ""
        self.page = SublandingPage(
            title="test",
            content=json.dumps(
                [
                    {
                        "type": "notification",
                        "value": {"body": "Incorrect Meta Description"},
                    }
                ]
            ),
        )
        test_context = self.page.get_context(self.request)
        result = test_context["meta_description"]
        self.assertEqual(expected, result)

    def test_get_context_sets_meta_description_strips_html_tags(self):
        expected = "Correct Meta Description"
        self.page = SublandingPage(
            title="test",
            header=json.dumps(
                [
                    {
                        "type": "hero",
                        "value": {"body": "<p></li>" + expected + "</li></p>"},
                    }
                ]
            ),
        )
        test_context = self.page.get_context(self.request)
        result = test_context["meta_description"]
        expectedWithSpaces = "  " + expected + "  "
        self.assertEqual(expectedWithSpaces, result)

    def test_get_context_sets_is_faq_page_to_false_without_faq(self):
        self.page = BrowsePage(
            title="test",
            content=json.dumps(
                [
                    {
                        "type": "expandable_group",
                        "value": {},
                    }
                ]
            ),
        )
        test_context = self.page.get_context(self.request)
        result = test_context["is_faq_page"]
        self.assertEqual(False, result)

    def test_get_context_sets_is_faq_page_to_true_with_faq_expandable(self):
        self.page = BrowsePage(
            title="test",
            content=json.dumps(
                [
                    {
                        "type": "expandable_group",
                        "value": {"is_faq": True},
                    }
                ]
            ),
        )
        test_context = self.page.get_context(self.request)
        result = test_context["is_faq_page"]
        self.assertEqual(True, result)

    def test_get_context_sets_is_faq_page_to_true_with_faq_group(self):
        self.page = BrowsePage(
            title="test",
            content=json.dumps(
                [
                    {
                        "type": "faq_group",
                        "value": {},
                    }
                ]
            ),
        )
        test_context = self.page.get_context(self.request)
        result = test_context["is_faq_page"]
        self.assertEqual(True, result)


class TestCFGOVPageTranslationActivation(TestCase):
    def test_english_page_serves_in_english(self):
        page = LandingPage(title="test", language="en")
        request = RequestFactory().get("/")
        response = page.serve(request)
        self.assertContains(response, "Search")

    def test_spanish_page_serves_in_spanish(self):
        page = LandingPage(title="test", language="es")
        request = RequestFactory().get("/")
        response = page.serve(request)
        self.assertContains(response, "Buscar")

    def test_english_page_serves_preview_in_english(self):
        page = LandingPage(title="test", language="en")
        response = page.make_preview_request()
        self.assertContains(response, "Search")

    def test_spanish_page_serves_preview_in_spanish(self):
        page = LandingPage(title="test", language="es")
        response = page.make_preview_request()
        self.assertContains(response, "Buscar")


class TestCFGOVPageQuerySet(TestCase):
    def setUp(self):
        default_site = Site.objects.get(is_default_site=True)
        self.live_host = default_site.hostname

    def check_live_counts(self, on_live_host):
        pages = CFGOVPage.objects
        self.assertEqual(pages.live().count(), on_live_host)

    def test_live_with_only_root_page(self):
        self.check_live_counts(on_live_host=1)

    def test_live_with_another_draft_page(self):
        page = CFGOVPage(title="test", slug="test", live=False)
        save_new_page(page)
        self.check_live_counts(on_live_host=1)

    def test_live_with_another_live_page(self):
        page = CFGOVPage(title="test", slug="test", live=True)
        save_new_page(page)
        self.check_live_counts(on_live_host=2)


class TestCFGOVPageMediaJSProperty(TestCase):
    """Tests how the page.media_js property pulls in child block JS."""

    def test_empty_page_has_no_media(self):
        self.assertEqual(CFGOVPage().media_js, [])

    def test_empty_page_has_no_page_js(self):
        self.assertEqual(CFGOVPage().page_js, [])

    def test_empty_page_has_no_streamfield_js(self):
        self.assertEqual(CFGOVPage().streamfield_media("js"), [])

    def test_page_pulls_in_child_block_media(self):
        page = CFGOVPage()
        page.sidefoot = blocks.StreamValue(
            page.sidefoot.stream_block,
            [
                {"type": "email_signup", "value": 1},
            ],
            True,
        )

        self.assertEqual(page.media_js, ["email-signup.js"])

    def test_doesnt_pull_in_media_for_nonexistent_child_blocks(self):
        page = BrowsePage()
        page.content = blocks.StreamValue(
            page.content.stream_block,
            [
                {
                    "type": "full_width_text",
                    "value": [],
                },
            ],
            True,
        )

        # The page media shouldn't add any additional files because of the
        # FullWidthText.
        self.assertEqual(page.media_js, [])


class TestCFGOVPageMediaCSSProperty(TestCase):
    """Tests how the page.media_css property pulls in child block CSS."""

    def test_empty_page_has_no_media(self):
        self.assertEqual(CFGOVPage().media_css, [])

    def test_empty_page_has_no_streamfield_css(self):
        self.assertEqual(CFGOVPage().streamfield_media("css"), [])

    def test_page_pulls_in_child_block_media(self):
        page = BrowsePage()
        page.content = blocks.StreamValue(
            page.content.stream_block,
            [
                {
                    "type": "simple_chart",
                    "value": {},
                }
            ],
            True,
        )
        page.sidefoot = blocks.StreamValue(
            page.sidefoot.stream_block,
            [
                {
                    "type": "sidebar_contact",
                    "value": {},
                },
            ],
            True,
        )

        self.assertEqual(
            page.media_css, ["sidebar-contact-info.css", "simple-chart.css"]
        )

    def test_doesnt_pull_in_media_for_nonexistent_child_blocks(self):
        page = BrowsePage()
        page.content = blocks.StreamValue(
            page.content.stream_block,
            [
                {
                    "type": "full_width_text",
                    "value": [],
                },
            ],
            True,
        )

        # The page media should only include the default BrowsePage media, and
        # shouldn't add any additional files because of the FullWithText.
        self.assertEqual(page.media_css, [])


class TestCFGOVPageCopy(TestCase):
    def setUp(self):
        self.site = Site.objects.first()
        self.root_page = self.site.root_page
        self.page_with_tags = CFGOVPage(
            title="Tagged", slug="tagged", live=True
        )
        save_new_page(self.page_with_tags, root=self.root_page)
        self.page_with_tags.tags.add("tag1")
        self.page_with_tags.authors.add("author1")
        self.page_with_tags.save()

    def check_tagged_page_copies_without_error(self):
        test_page = self.page_with_tags
        new_page = test_page.copy(
            update_attrs={
                "slug": f"{test_page.slug}-copy",
                "title": f"{test_page.title} COPY",
            }
        )
        self.assertEqual(new_page.title, "Tagged COPY")


class TestCFGOVPageBreadcrumbs(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.site = Site.objects.first()
        self.root_page = self.site.root_page

        self.top_level_page = CFGOVPage(title="top", slug="top", live=True)
        save_new_page(self.top_level_page, root=self.root_page)

        self.second_level_page = CFGOVPage(
            title="second", slug="second", live=True
        )
        save_new_page(self.second_level_page, root=self.top_level_page)

        self.third_level_page = CFGOVPage(
            title="third", slug="third", live=True
        )
        save_new_page(self.third_level_page, root=self.second_level_page)

    def test_get_breadcrumbs_forced_homepage_descendant(self):
        request = self.factory.get("/top/second")
        self.top_level_page.force_breadcrumbs = True
        self.top_level_page.save()
        self.assertIn(
            "top",
            [p.slug for p in self.second_level_page.get_breadcrumbs(request)],
        )

    def test_get_breadcrumbs_no_homepage_descendant(self):
        request = self.factory.get("/top/second")
        self.assertNotIn(
            "top",
            [p.slug for p in self.second_level_page.get_breadcrumbs(request)],
        )

    def test_get_breadcrumbs_two_levels_deep(self):
        request = self.factory.get("/top/second/third")
        self.assertNotIn(
            "top",
            [p.slug for p in self.third_level_page.get_breadcrumbs(request)],
        )
        self.assertIn(
            "second",
            [p.slug for p in self.third_level_page.get_breadcrumbs(request)],
        )


class TestCFGOVPageTranslations(TestCase):
    def setUp(self):
        self.site_root = Site.objects.get(is_default_site=True).root_page

    def make_page(self, **kwargs):
        language = kwargs.pop("language", "en")
        page = BrowsePage(
            title="test",
            slug=language,
            language=language,
            **kwargs,
        )
        self.site_root.add_child(instance=page)
        return page

    def test_pages_without_translations(self):
        page_en = self.make_page(language="en")
        self.assertEqual(page_en.get_translations().count(), 1)
        self.assertEqual(page_en.get_translations()[0].pk, page_en.pk)
        self.assertEqual(page_en.get_translations(inclusive=False).count(), 0)

        page_es = self.make_page(language="es")
        self.assertEqual(page_es.get_translations().count(), 1)
        self.assertEqual(page_es.get_translations()[0].pk, page_es.pk)
        self.assertEqual(page_es.get_translations(inclusive=False).count(), 0)

    def test_pages_with_translations(self):
        page_en = self.make_page(language="en")
        page_es = self.make_page(language="es", english_page=page_en)

        self.assertEqual(page_en.get_translations().count(), 2)
        self.assertEqual(page_en.get_translations().first().pk, page_en.pk)
        self.assertEqual(page_en.get_translations().last().pk, page_es.pk)

        self.assertEqual(page_en.get_translations(inclusive=False).count(), 1)
        self.assertEqual(
            page_en.get_translations(inclusive=False).first().pk, page_es.pk
        )

        self.assertEqual(page_es.get_translations().count(), 2)
        self.assertEqual(page_es.get_translations().first().pk, page_en.pk)
        self.assertEqual(page_es.get_translations().last().pk, page_es.pk)

        self.assertEqual(page_es.get_translations(inclusive=False).count(), 1)
        self.assertEqual(
            page_es.get_translations(inclusive=False).first().pk, page_en.pk
        )

    def test_page_translation_ordering(self):
        page_en = self.make_page(language="en")
        page_es = self.make_page(language="es", english_page=page_en)
        self.make_page(language="ht", english_page=page_en)
        self.make_page(language="ko", english_page=page_en)

        self.assertSequenceEqual(
            page_en.get_translations().values_list("language", flat=True),
            ["en", "es", "ko", "ht"],
        )
        self.assertSequenceEqual(
            page_es.get_translations().values_list("language", flat=True),
            ["en", "es", "ko", "ht"],
        )

    def test_page_not_live_excluded(self):
        page_en = self.make_page(language="en")
        self.make_page(language="es", english_page=page_en, live=False)
        self.assertEqual(page_en.get_translations().count(), 1)
        self.assertEqual(page_en.get_translations().first().pk, page_en.pk)

    def test_pages_not_in_site_excluded(self):
        page_en = self.make_page(language="en")

        page_es = BrowsePage(
            title="test",
            slug="es",
            language="es",
            english_page=page_en,
        )
        Page.get_first_root_node().add_child(instance=page_es)

        # Pages in a site only return linked pages in the same site.
        self.assertEqual(page_en.get_translations().count(), 1)
        self.assertEqual(page_en.get_translations().first().pk, page_en.pk)

        # Pages that are not in any site return all linked pages.
        self.assertEqual(page_es.get_translations().count(), 2)
        self.assertEqual(page_es.get_translations().first().pk, page_en.pk)
        self.assertEqual(page_es.get_translations().last().pk, page_es.pk)

    def test_new_english_page_without_primary_key(self):
        new_page_en = BrowsePage(language="en")
        self.assertEqual(new_page_en.get_translations().count(), 1)
        self.assertEqual(
            new_page_en.get_translations().first().pk, new_page_en.pk
        )
        self.assertEqual(
            new_page_en.get_translations(inclusive=False).count(), 0
        )

    def test_new_spanish_page_without_primary_key(self):
        new_page_es = BrowsePage(language="es")
        self.assertEqual(new_page_es.get_translations().count(), 1)
        self.assertEqual(
            new_page_es.get_translations().first().pk, new_page_es.pk
        )
        self.assertEqual(
            new_page_es.get_translations(inclusive=False).count(), 0
        )

        page_en = self.make_page(language="en")
        new_page_es.english_page = page_en
        self.assertEqual(new_page_es.get_translations().count(), 2)
        self.assertEqual(new_page_es.get_translations().first().pk, page_en.pk)
        self.assertEqual(
            new_page_es.get_translations().last().pk, new_page_es.pk
        )
        self.assertEqual(
            new_page_es.get_translations(inclusive=False).count(), 1
        )
        self.assertEqual(new_page_es.get_translations().first().pk, page_en.pk)

    def test_page_get_translation_links(self):
        page_en = self.make_page(language="en")
        self.make_page(language="es", english_page=page_en)

        request = RequestFactory().get("/")

        self.assertEqual(
            page_en.get_translation_links(request),
            [
                {
                    "href": "/en/",
                    "language": "en",
                    "text": "English",
                },
                {
                    "href": "/es/",
                    "language": "es",
                    "text": "Spanish",
                },
            ],
        )

        self.assertEqual(
            page_en.get_translation_links(request, inclusive=False),
            [
                {
                    "href": "/es/",
                    "language": "es",
                    "text": "Spanish",
                },
            ],
        )
