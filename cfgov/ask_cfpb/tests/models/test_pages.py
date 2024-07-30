import json
import tempfile
from unittest import mock

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import HttpRequest
from django.test import SimpleTestCase, TestCase, override_settings
from django.test.client import RequestFactory
from django.urls import reverse
from django.utils import timezone, translation

from wagtail.models import Site

from model_bakery import baker

from ask_cfpb.documents import AnswerPageDocument
from ask_cfpb.models.django import (
    ENGLISH_PARENT_SLUG,
    SPANISH_PARENT_SLUG,
    Answer,
    Category,
    NextStep,
)
from ask_cfpb.models.pages import (
    REUSABLE_TEXT_TITLES,
    AnswerLandingPage,
    AnswerPage,
    PortalSearchPage,
    TagResultsPage,
    strip_html,
    validate_page_number,
)
from ask_cfpb.models.snippets import GlossaryTerm
from v1.models import (
    CFGOVImage,
    HomePage,
    PortalCategory,
    PortalTopic,
    SublandingPage,
)


TEMPDIR = tempfile.gettempdir()

now = timezone.now()


class TestStripHTML(SimpleTestCase):
    def test_strip_html_headline_separation(self):
        """Make sure stripped markup doesn't jam headlines into text."""
        markup = (
            "<h2><span>"
            "What to know about consolidating debt with a reverse mortgage"
            "</span></h2>"
            "<p></p><ul><li><span>"
            "A reverse mortgage is not free money."
            "</span></li></ul>"
        )
        self.assertNotIn("mortgageA", strip_html(markup))


class AnswerStringTest(TestCase):
    def test_answer_string_method(self):
        test_answer = Answer(question="Test question?")
        test_answer.save()
        self.assertEqual(test_answer.__str__(), test_answer.question)


class PortalSearchPageTest(TestCase):
    fixtures = [
        "ask_tests",
        "portal_topics",
        "portal_categories",
        "test_ask_tags",
    ]

    def setUp(self):
        def create_page(model, title, slug, parent, language="en", **kwargs):
            new_page = model(
                live=False, language=language, title=title, slug=slug
            )
            for k, v in kwargs.items():
                setattr(new_page, k, v)
            parent.add_child(instance=new_page)
            new_page.save()
            new_page.save_revision(user=self.test_user).publish()
            return new_page

        self.site = Site.objects.get(is_default_site=True)
        self.ROOT_PAGE = self.site.root_page
        self.portal_topic = PortalTopic.objects.get(pk=1)
        self.portal_topic2 = PortalTopic.objects.get(pk=2)
        self.test_user = User.objects.last()
        self.english_ask_parent = create_page(
            AnswerLandingPage, "Ask CFPB", "ask-cfpb", self.ROOT_PAGE
        )
        self.english_portal_parent = create_page(
            SublandingPage, "Consumer Tools", "consumer-tools", self.ROOT_PAGE
        )
        self.english_portal = create_page(
            SublandingPage,
            "Auto loans",
            "auto-loans",
            self.english_portal_parent,
            portal_topic_id=1,
        )
        self.english_portal2 = create_page(
            SublandingPage,
            "Bank accounts",
            "bank-accounts",
            self.english_portal_parent,
            portal_topic_id=2,
        )
        self.english_search_page = create_page(
            PortalSearchPage,
            "Auto loan answers",
            "answers",
            self.english_portal,
            portal_topic_id=1,
        )
        self.english_search_page2 = create_page(
            PortalSearchPage,
            "Bank account answers",
            "answers",
            self.english_portal2,
            portal_topic_id=2,
        )
        self.spanish_parent = create_page(
            SublandingPage,
            "Obtener respuestas",
            "obtener-respuestas",
            self.ROOT_PAGE,
            language="es",
        )
        self.spanish_portal = create_page(
            SublandingPage,
            "Préstamos para vehículos",
            "prestamos-para-vehiculos",
            self.spanish_parent,
            language="es",
            portal_topic_id=1,
        )
        self.spanish_search_page = create_page(
            PortalSearchPage,
            "Préstamos para vehículos respuestas",
            "respuestas",
            self.spanish_portal,
            language="es",
            portal_topic_id=1,
        )
        self.answer_page = create_page(
            AnswerPage,
            "English auto-loans question-8888?",
            "english-auto-loans-question-en-8888",
            self.english_ask_parent,
            featured=True,
        )
        self.answer_page.portal_topic.add(self.portal_topic)
        self.answer_page.save()
        self.answer_page2 = create_page(
            AnswerPage,
            "English banks question-8889?",
            "english-banks-question-en-8889",
            self.english_ask_parent,
            featured=True,
        )
        self.answer_page.portal_topic.add(self.portal_topic2)
        self.answer_page.save()
        self.answer_page_es = create_page(
            AnswerPage,
            "Spanish test question-es-9999?",
            "spanish_test-question-es-9999",
            self.spanish_parent,
            language="es",
            primary_portal_topic_id=1,
        )

    def test_bad_category_value_raises_404(self):
        page = self.english_search_page
        url = page.url + page.reverse_subpage(
            "portal_category_page", kwargs={"category": "how-to-gui"}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_get_ask_breadcrumbs_with_portal(self):
        response = self.client.get(self.answer_page_es.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data["breadcrumb_items"]), 1)
        self.assertEqual(
            response.context_data["breadcrumb_items"][0]["title"],
            self.answer_page_es.primary_portal_topic.heading_es,
        )

    def test_get_ask_breadcrumbs_with_draft_portal(self):
        self.spanish_portal.unpublish()
        self.spanish_portal.save()
        response = self.client.get(self.answer_page_es.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data["breadcrumb_items"]), 1)
        self.assertEqual(
            response.context_data["breadcrumb_items"][0]["title"],
            self.spanish_search_page.title,
        )
        self.spanish_portal.save_revision(user=self.test_user).publish()

    def test_get_english_topic_heading(self):
        page = self.english_search_page
        self.assertEqual(page.get_heading(), "Auto loans")

    def test_get_english_category_heading(self):
        page = self.english_search_page
        page.portal_category = PortalCategory.objects.get(
            heading="How-to guides"
        )
        self.assertEqual(page.get_heading(), "How-to guides")

    def test_get_spanish_topic_heading(self):
        page = self.spanish_search_page
        self.assertEqual(page.get_heading(), "Préstamos para vehículos")

    def test_get_spanish_category_heading(self):
        page = self.spanish_search_page
        page.portal_category = PortalCategory.objects.get(
            heading_es="Paso a paso"
        )
        self.assertEqual(page.get_heading(), "Paso a paso")

    def test_english_portal_title(self):
        test_page = self.english_search_page
        self.assertEqual(str(test_page), test_page.title)
        self.assertEqual(test_page.portal_topic, PortalTopic.objects.get(pk=1))

    @mock.patch.object(AnswerPageDocument, "search")
    def test_english_category_title(self, mock_search):
        page = self.english_search_page
        url = page.url + page.reverse_subpage(
            "portal_category_page", kwargs={"category": "how-to-guides"}
        )
        response = self.client.get(url)
        self.assertEqual(
            response.context_data.get("page").title, "Auto loans how-to guides"
        )

    @mock.patch.object(AnswerPageDocument, "search")
    def test_spanish_category_title(self, mock_search):
        page = self.spanish_search_page
        url = page.url + page.reverse_subpage(
            "portal_category_page", kwargs={"category": "paso-a-paso"}
        )
        response = self.client.get(url)
        self.assertEqual(
            response.context_data.get("page").title,
            "Préstamos para vehículos paso a paso",
        )

    def test_category_map_length(self):
        self.assertEqual(
            len(self.english_search_page.category_map),
            PortalCategory.objects.count(),
        )

    def test_category_map_sort_order(self):
        mapping = self.english_search_page.category_map
        self.assertEqual(
            [p.pk for p in PortalCategory.objects.all()],
            [category.pk for slug, category in mapping.items()],
        )

    def test_results_message_no_category_no_search_term(self):
        msg = self.english_search_page.results_message(10, "Auto loans", "")
        self.assertEqual(msg, "Showing 10 results  within auto loans")

    def test_results_message_no_category_with_search_term(self):
        msg = self.english_search_page.results_message(
            1, "Auto loans", "hoodoo"
        )
        self.assertEqual(
            msg, 'Showing  1 result for "hoodoo" within auto loans'
        )

    def test_results_message_with_category_no_search_term(self):
        self.english_search_page.portal_category = PortalCategory.objects.get(
            heading="How-to guides"
        )
        msg = self.english_search_page.results_message(10, "How-to guides", "")
        self.assertEqual(msg, "Showing 10 results within how-to guides")

    def test_results_message_with_category_and_search_term(self):
        self.english_search_page.portal_category = PortalCategory.objects.get(
            heading="How-to guides"
        )
        msg = self.english_search_page.results_message(
            1, "How-to guides", "hoodoo"
        )
        self.assertEqual(
            msg,
            "Showing  1 result for &quot;hoodoo&quot; within how-to guides"
            '<span class="results-link"><a href="../?search_term=hoodoo">'
            "See all results within auto loans</a></span>",
        )

    @mock.patch.object(AnswerPageDocument, "search")
    def test_portal_topic_page_200(self, mock_search):
        page = self.english_search_page
        response = self.client.get(page.url)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(AnswerPageDocument, "search")
    def test_portal_category_page_calls_search(self, mock_search):
        page = self.english_search_page
        portal_search_url = page.url + page.reverse_subpage(
            "portal_category_page", kwargs={"category": "basics"}
        )
        mock_search.filter.return_value = {
            "search_term": "hipotatoes",
            "suggestion": "potatoes",
            "results": [],
        }
        response = self.client.get(portal_search_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_search.call_count, 1)

    @mock.patch.object(AnswerPageDocument, "search")
    def test_spanish_portal_search_page_renders(self, mock_search):
        page = self.spanish_search_page
        portal_search_url = page.url + page.reverse_subpage(
            "portal_category_page", kwargs={"category": "paso-a-paso"}
        )
        mock_search.filter.return_value = {
            "search_term": "hipotacos",
            "suggestion": "hipotecas",
            "results": [],
        }
        response = self.client.get(portal_search_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_search.call_count, 1)

    @mock.patch.object(AnswerPageDocument, "search")
    def test_portal_topic_page_with_no_hits_same_suggestion(self, mock_search):
        term = "hipotatoes"
        mock_search.suggest.return_value = {
            "search_term": term,
            "suggestion": None,
            "results": [],
        }
        mock_search.search.return_value = {
            "search_term": term,
            "suggestion": None,
            "results": [],
        }
        page = self.english_search_page
        base_url = page.url
        url = f"{base_url}?search_term={term}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_search.call_count, 1)

    @mock.patch.object(AnswerPageDocument, "search")
    def test_portal_topic_page_with_no_hits_with_suggestion(self, mock_search):
        term = "hipotatoes"
        mock_search.suggest.return_value = {
            "search_term": term,
            "suggestion": "potatoes",
            "results": ["hit1", "hit2"],
        }
        mock_search.search.return_value = {
            "search_term": term,
            "suggestion": "potatoes",
            "results": ["hit1", "hit2"],
        }
        page = self.english_search_page
        base_url = page.url
        url = f"{base_url}?search_term={term}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_search.call_count, 1)

    @mock.patch.object(AnswerPageDocument, "search")
    def test_portal_category_page_with_no_hits_with_suggestion(
        self, mock_search
    ):
        term = "hoodoo"
        mock_search.suggest.return_value = {
            "search_term": term,
            "suggestion": "hoodunit",
            "results": ["hit1", "hit2"],
        }
        page = self.english_search_page
        base_url = page.url + page.reverse_subpage(
            "portal_category_page", kwargs={"category": "how-to-guides"}
        )
        url = f"{base_url}?search_term={term}"
        with override_settings(
            FLAGS={"ASK_SEARCH_TYPOS": [("boolean", True)]}
        ):
            response = self.client.get(url)
            self.assertEqual(response.context_data["search_term"], term)
            self.assertEqual(response.status_code, 200)

    @mock.patch.object(AnswerPageDocument, "search")
    def test_portal_category_page_same_suggestion(self, mock_search):
        term = "hoodoo"
        mock_search.suggest.return_value = {
            "search_term": term,
            "suggestion": term,
            "results": [],
        }
        page = self.english_search_page
        base_url = page.url + page.reverse_subpage(
            "portal_category_page", kwargs={"category": "how-to-guides"}
        )
        url = f"{base_url}?search_term={term}"
        response = self.client.get(url)
        self.assertEqual(response.context_data["search_term"], term)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(AnswerPageDocument, "search")
    def test_portal_topic_page_suggestion(self, mock_search):
        term = "hoodoo"
        mock_search.suggest.return_value = {
            "search_term": term,
            "suggestion": "hoodunit",
            "results": [],
        }
        page = self.english_search_page
        base_url = page.url
        url = f"{base_url}?search_term={term}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data["search_term"], term)

    def test_get_glossary_terms(self):
        page = self.english_search_page
        glossary_term = GlossaryTerm(
            name_en="Escrow",
            definition_en="Definition",
            portal_topic=page.portal_topic,
        )
        glossary_term.save()
        terms = page.get_glossary_terms()
        self.assertEqual(next(terms).name("en"), "Escrow")

    def test_portal_category_page_key_terms(self):
        page = self.english_search_page
        glossary_term = GlossaryTerm(
            name_en="Amortization",
            definition_en="Definition",
            portal_topic=page.portal_topic,
        )
        glossary_term.save()
        url = f"{page.url}key-terms/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Amortization")

    def test_portal_category_page_key_terms_spanish(self):
        page = self.spanish_search_page
        glossary_term = GlossaryTerm(
            name_en="Amortization",
            name_es="Amortización",
            definition_es="Definición",
            portal_topic=page.portal_topic,
        )
        glossary_term.save()
        url = f"{page.url}palabras-claves/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Amortización")

    def make_page(self, **kwargs):
        language = kwargs.pop("language", "en")
        page = PortalSearchPage(
            title="test",
            slug=language,
            language=language,
            **kwargs,
        )
        self.ROOT_PAGE.add_child(instance=page)
        return page

    def test_portal_page_translations(self):
        category = PortalCategory(
            heading="Key terms", heading_es="Palabras claves"
        )
        category.save()
        page_en = self.make_page(language="en")
        page_es = self.make_page(language="es", english_page=page_en)

        page_en.portal_category = category
        page_es.portal_category = category

        request = RequestFactory().get("/")

        self.assertEqual(
            page_en.get_translation_links(request),
            [
                {
                    "href": "/en/key-terms/",
                    "language": "en",
                    "text": "English",
                },
                {
                    "href": "/es/palabras-claves/",
                    "language": "es",
                    "text": "Spanish",
                },
            ],
        )


class AnswerPageTest(TestCase):
    fixtures = ["ask_tests", "portal_topics"]

    def create_answer_page(self, **kwargs):
        page = AnswerPage(
            slug="mock-answer-page-en-1234", title="Mock answer page title"
        )
        self.english_parent_page.add_child(instance=page)
        return page

    def setUp(self):
        self.test_user = User.objects.get(pk=1)
        self.ROOT_PAGE = HomePage.objects.get(slug="cfgov")
        self.category = baker.make(
            Category, name="stub_cat", name_es="que", slug="stub-cat"
        )
        self.category.save()
        self.test_image = baker.make(CFGOVImage)
        self.test_image2 = baker.make(CFGOVImage)
        self.next_step = baker.make(NextStep, title="stub_step")
        self.portal_topic = baker.make(
            PortalTopic, heading="test topic", heading_es="prueba tema"
        )
        page_clean = mock.patch("ask_cfpb.models.pages.CFGOVPage.clean")
        page_clean.start()
        self.addCleanup(page_clean.stop)
        self.portal_page = SublandingPage(
            title="test portal page",
            slug="test-portal-page",
            portal_topic=self.portal_topic,
            language="en",
        )
        self.ROOT_PAGE.add_child(instance=self.portal_page)
        self.portal_page.save()
        self.portal_page.save_revision().publish()
        self.portal_page_es = SublandingPage(
            title="test portal page",
            slug="test-portal-page-es",
            portal_topic=self.portal_topic,
            language="es",
        )
        self.ROOT_PAGE.add_child(instance=self.portal_page_es)
        self.portal_page_es.save()
        self.portal_page_es.save_revision().publish()

        self.english_parent_page = AnswerLandingPage(
            title="Ask CFPB",
            slug=ENGLISH_PARENT_SLUG,
            language="en",
            live=True,
        )
        self.ROOT_PAGE.add_child(instance=self.english_parent_page)

        self.spanish_parent_page = AnswerLandingPage(
            title="Obtener respuestas",
            slug=SPANISH_PARENT_SLUG,
            language="es",
            live=True,
        )
        self.ROOT_PAGE.add_child(instance=self.spanish_parent_page)

        self.tag_results_page_en = TagResultsPage(
            title="Tag results page",
            slug="search-by-tag",
            language="en",
            live=True,
        )
        self.ROOT_PAGE.add_child(instance=self.tag_results_page_en)

        self.tag_results_page_es = TagResultsPage(
            title="Tag results page",
            slug="buscar-por-etiqueta",
            language="es",
            live=True,
        )
        self.ROOT_PAGE.add_child(instance=self.tag_results_page_es)
        self.answer1234 = Answer(id=1234)
        self.answer1234.save()
        self.page1 = AnswerPage(
            language="en",
            answer_base=self.answer1234,
            slug="mock-question-en-1234",
            title="Mock question1",
            answer_content=json.dumps(
                [
                    {
                        "type": "text",
                        "value": {
                            "anchor_tag": "",
                            "content": "Mock answer 1",
                        },
                    }
                ]
            ),
            question="Mock question1",
            search_tags="hippodrome",
        )
        self.english_parent_page.add_child(instance=self.page1)
        self.page1.save_revision().publish()
        self.page1_es = AnswerPage(
            language="es",
            slug="mock-spanish-question1-es-1234",
            title="Mock Spanish question1",
            answer_base=self.answer1234,
            answer_content=json.dumps(
                [
                    {
                        "type": "text",
                        "value": {
                            "anchor_tag": "",
                            "content": "Mock Spanish answer",
                        },
                    }
                ]
            ),
            question="Mock Spanish question1",
            search_tags="hipotecas",
        )
        self.spanish_parent_page.add_child(instance=self.page1_es)
        self.page1_es.save_revision().publish()
        self.answer5678 = Answer(id=5678)
        self.answer5678.save()
        self.page2 = AnswerPage(
            language="en",
            slug="mock-question2-en-5678",
            title="Mock question2",
            answer_base=self.answer5678,
            answer_content=json.dumps(
                [
                    {
                        "type": "text",
                        "value": {
                            "anchor_tag": "",
                            "content": "Mock answer 2",
                        },
                    }
                ]
            ),
            question="Mock question2",
            search_tags="hippodrome",
        )
        self.english_parent_page.add_child(instance=self.page2)
        self.page2.save_revision().publish()

    def test_tag_results_page_templates(self):
        self.assertEqual(
            self.tag_results_page_es.get_template(HttpRequest()),
            self.tag_results_page_en.get_template(HttpRequest()),
        )

    def test_tag_results_page_context_language(self):
        context = self.tag_results_page_es.get_context(HttpRequest())
        self.assertEqual(
            context.get("breadcrumb_items")[0]["title"], "Obtener respuestas"
        )

    def test_answer_content_preview_word(self):
        """answer_content_preview returns truncated text by word count

        And without HTML tags.
        """

        page = self.page1
        page.answer_content = json.dumps(
            [
                {
                    "type": "video_player",
                    "id": "402b933b",
                    "value": {
                        "video_url": "https://www.youtube.com/embed/wcQ1a_Gg8tI"
                    },
                },
                {
                    "type": "text",
                    "id": "402b933c",
                    "value": {
                        "content": (
                            "<p><span>"
                            "This is more than forty words: "
                            "word word word word word word word word word "
                            "word word word word word word word word word "
                            "word word word word word word word word word "
                            "word word word word word word word word word "
                            "too-many."
                            "</span></p>"
                        )
                    },
                },
            ]
        )
        self.assertTrue(
            page.answer_content_preview().endswith("word word ...")
        )

    def test_answer_content_preview_char(self):
        """answer_content_preview returns truncated text by character count

        And without HTML tags.
        """

        page = self.page1
        page.answer_content = json.dumps(
            [
                {
                    "type": "video_player",
                    "id": "402b933b",
                    "value": {
                        "video_url": "https://www.youtube.com/embed/wcQ1a_Gg8tI"
                    },
                },
                {
                    "type": "text",
                    "id": "402b933c",
                    "value": {
                        "content": (
                            "<p><span>"
                            "This a word with more than 255 characters: "
                            "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                            "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                            "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                            "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                            "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                            "char char char char char char char char char "
                            "char char char char char char char char char "
                            "char char char char char char char char char "
                            "char char char char char char char char char "
                            "too-many."
                            "</span></p>"
                        )
                    },
                },
            ]
        )
        self.assertTrue(page.answer_content_preview().endswith(" ..."))

    def test_english_page_context(self):
        from ask_cfpb.models.pages import get_reusable_text_snippet
        from v1.models.snippets import ReusableText

        rt = ReusableText(title="About us (For consumers)")
        rt.save()
        page = self.page1
        page.language = "en"
        page.save()
        test_context = page.get_context(HttpRequest())
        self.assertEqual(
            test_context["about_us"],
            get_reusable_text_snippet("About us (For consumers)"),
        )

    def test_get_meta_description(self):
        page = self.page1
        # Defaults to standard answer content
        self.assertEqual(page.get_meta_description(), "Mock answer 1")

        # Second fallback is truncated answer_content text block
        page.answer_content = json.dumps(
            [
                {
                    "type": "video_player",
                    "id": "402b933b",
                    "value": {
                        "video_url": "https://www.youtube.com/embed/wcQ1a_Gg8tI"
                    },
                },
                {
                    "type": "text",
                    "id": "402b933c",
                    "value": {
                        "content": (
                            "<p><span>"
                            "This is more than forty words: "
                            "word word word word word word word word word "
                            "word word word word word word word word word "
                            "word word word word word word word word word "
                            "word word word word word word word word word "
                            "too-many."
                            "</span></p>"
                        )
                    },
                },
            ]
        )
        self.assertTrue(page.get_meta_description().endswith("word word ..."))

        # First fallback is the short_answer
        page.short_answer = "Test short answer"
        self.assertEqual(page.get_meta_description(), page.short_answer)

        # First choice is the search_description
        page.search_description = "Test search description"
        self.assertEqual(page.get_meta_description(), page.search_description)

    def test_routable_tag_page_base_returns_404(self):
        page = self.tag_results_page_en
        response = self.client.get(page.url + page.reverse_subpage("tag_base"))
        self.assertEqual(response.status_code, 404)

    def test_routable_tag_page_handles_bad_tag(self):
        page = self.tag_results_page_en
        response = self.client.get(
            page.url
            + page.reverse_subpage(
                "tag_search", kwargs={"tag": "hippopotamus"}
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_routable_tag_page_handles_bad_pagination(self):
        page = self.tag_results_page_en
        response = self.client.get(
            page.url
            + page.reverse_subpage("tag_search", kwargs={"tag": "hippodrome"}),
            {"page": "100"},
        )
        self.assertEqual(response.status_code, 200)

    def test_routable_tag_page_valid_tag_returns_200(self):
        page = self.tag_results_page_en
        response = self.client.get(
            page.url
            + page.reverse_subpage("tag_search", kwargs={"tag": "hippodrome"})
        )
        self.assertEqual(response.status_code, 200)

    def test_routable_tag_page_returns_url_suffix(self):
        page = self.tag_results_page_en
        response = page.reverse_subpage(
            "tag_search", kwargs={"tag": "hippodrome"}
        )
        self.assertEqual(response, "hippodrome/")

    def test_view_answer_exact_slug(self):
        page = self.page1
        page.slug = "mock-answer-en-1234"
        page.save()
        revision = page.save_revision()
        revision.publish()
        response = self.client.get(
            reverse("ask-english-answer", args=["mock-answer", "en", 1234])
        )
        self.assertEqual(response.status_code, 200)

    def test_view_answer_301_for_healed_slug(self):
        page = self.page1
        revision = page.save_revision()
        revision.publish()
        response = self.client.get(
            reverse("ask-english-answer", args=["mock-slug", "en", 1234])
        )
        self.assertEqual(response.status_code, 301)

    def test_spanish_answer_page_handles_referrer_with_unicode_accents(self):
        referrer_unicode = (
            "https://www.consumerfinance.gov/es/obtener-respuestas/"
            "buscar-por-etiqueta/empresas_de_informes_de_cr\xe9dito/"
        )
        spanish_page = self.page1_es
        request = HttpRequest()
        request.POST["referrer"] = referrer_unicode
        response = spanish_page.serve(request)
        self.assertEqual(response.status_code, 200)

    def test_page_string_no_base(self):
        test_page = self.create_answer_page()
        result = test_page.__str__()
        self.assertEqual(result, test_page.title)

    def test_page_string_with_base(self):
        page = self.page1
        self.assertTrue(page.answer_base)
        result = page.__str__()
        self.assertEqual(result, f"{page.answer_base.pk}: {page.title}")

    def test_search_tags(self):
        """Test the list produced by page.clean_search_tags()."""
        page = self.page1
        page.search_tags = "Chutes, Ladders"
        page.save_revision().publish()
        taglist = page.clean_search_tags
        for name in ["Chutes", "Ladders"]:
            self.assertIn(name, taglist)

    def test_english_header_and_footer(self):
        english_answer_page_response = self.client.get(
            reverse("ask-english-answer", args=["mock-question", "en", 1234])
        )
        self.assertContains(
            english_answer_page_response, "An official website of the"
        )
        self.assertContains(
            english_answer_page_response, "United States government"
        )
        self.assertNotContains(
            english_answer_page_response, "Un sitio web oficial"
        )
        self.assertNotContains(
            english_answer_page_response,
            "gobierno federal de los Estados Unidos",
        )
        self.assertContains(
            english_answer_page_response, "https://www.usa.gov/"
        )
        self.assertNotContains(
            english_answer_page_response, "https://www.usa.gov/es/"
        )

    def test_spanish_header_and_footer(self):
        spanish_answer_page_response = self.client.get(
            reverse(
                "ask-spanish-answer",
                args=["mock-spanish-question1", "es", 1234],
            )
        )
        self.assertContains(
            spanish_answer_page_response, "Un sitio web oficial"
        )
        self.assertContains(
            spanish_answer_page_response,
            "gobierno federal de los Estados Unidos",
        )
        self.assertNotContains(
            spanish_answer_page_response, "An official website of the"
        )
        self.assertNotContains(
            spanish_answer_page_response, "United States government"
        )
        self.assertContains(
            spanish_answer_page_response, "https://www.usa.gov/es/"
        )
        self.assertNotContains(
            spanish_answer_page_response, 'https://www.usa.gov/"'
        )

    def test_category_str(self):
        category = self.category
        self.assertEqual(category.__str__(), category.name)

    def test_nextstep_str(self):
        next_step = self.next_step
        self.assertEqual(next_step.__str__(), next_step.title)

    def test_status_string(self):
        with translation.override("en"):
            page1 = self.page1
            self.assertEqual(page1.status_string, "live + draft")

    def test_get_ask_breadcrumbs(self):
        from ask_cfpb.models import get_ask_breadcrumbs

        breadcrumbs = get_ask_breadcrumbs()
        self.assertEqual(len(breadcrumbs), 1)
        self.assertEqual(breadcrumbs[0]["title"], "Ask CFPB")

    def test_answer_language_page_exists(self):
        self.assertEqual(self.answer5678.english_page, self.page2)

    def test_answer_language_page_nonexistent(self):
        self.assertEqual(self.answer5678.spanish_page, None)

    def test_get_reusable_text_snippet(self):
        from ask_cfpb.models import get_reusable_text_snippet
        from v1.models.snippets import ReusableText

        test_snippet = ReusableText.objects.create(title="Test Snippet")
        self.assertEqual(
            get_reusable_text_snippet("Test Snippet"), test_snippet
        )

    def test_get_nonexistent_reusable_text_snippet(self):
        from ask_cfpb.models import get_reusable_text_snippet

        self.assertEqual(
            get_reusable_text_snippet("Nonexistent Snippet"), None
        )

    def test_get_about_us_english_standard_text(self):
        from ask_cfpb.models import get_standard_text
        from v1.models.snippets import ReusableText

        snippet_title = REUSABLE_TEXT_TITLES["about_us"]["en"]
        test_snippet = ReusableText.objects.create(title=snippet_title)
        self.assertEqual(get_standard_text("en", "about_us"), test_snippet)

    def test_social_sharing_image_used(self):
        from v1.models.images import CFGOVImage

        image = CFGOVImage.objects.last()
        page = self.page1
        page.social_sharing_image = image
        page.save_revision(user=self.test_user).publish()
        self.assertEqual(page.meta_image, image)

    def test_answer_meta_image_undefined(self):
        """Answer page's meta image is undefined if social image is
        not provided
        """
        answer = Answer()
        answer.save()
        page = self.create_answer_page(answer_base=answer)
        self.assertIsNone(page.meta_image)

    def test_answer_meta_image_uses_category_image_if_no_social_image(self):
        """Answer page's meta image is its category's image"""
        category = baker.make(Category, category_image=self.test_image)
        page = self.page1
        page.category.add(category)
        page.save_revision()
        self.assertEqual(page.meta_image, self.test_image)

    def test_validate_pagination_number(self):
        paginator = Paginator([{"fake": "results"}] * 30, 25)
        request = HttpRequest()
        self.assertEqual(validate_page_number(request, paginator), 1)
        request.GET.update({"page": "2"})
        self.assertEqual(validate_page_number(request, paginator), 2)
        request = HttpRequest()
        request.GET.update({"page": "1000"})
        self.assertEqual(validate_page_number(request, paginator), 1)
        request = HttpRequest()
        request.GET.update({"page": "<script>Boo</script>"})
        self.assertEqual(validate_page_number(request, paginator), 1)

    def test_validate_uniqueness_of_language_and_answer(self):
        answer = baker.make(Answer)
        answer.save()

        page = AnswerPage(slug="question-en", title="Original question?")
        self.ROOT_PAGE.add_child(instance=page)
        page.answer_base = answer
        page.full_clean()
        page.save()

        dup_page = AnswerPage(
            slug="dup-question-en", title="Duplicate question?"
        )
        dup_page.answer_base = answer

        with self.assertRaises(ValidationError):
            dup_page.full_clean()


class AnswerPageContextTests(TestCase):
    def setUp(self):
        self.request = HttpRequest()
        self.site_root = Site.objects.get(is_default_site=True).root_page

    def make_portal_topic_and_page(self, name):
        topic = PortalTopic.objects.create(heading=name, heading_es=name)
        page = SublandingPage(title=name, slug=name, portal_topic=topic)
        self.site_root.add_child(instance=page)
        return topic, page

    def test_portal_page_no_portal_topics(self):
        page = AnswerPage()
        context = page.get_context(self.request)
        self.assertIsNone(context["portal_page"])

    def test_portal_page_primary_topic(self):
        topic, portal_page = self.make_portal_topic_and_page("test")
        page = AnswerPage(primary_portal_topic=topic)
        context = page.get_context(self.request)
        self.assertEqual(context["portal_page"], portal_page)

    def test_portal_page_no_primary_topic_single_portal_topic(self):
        topic, portal_page = self.make_portal_topic_and_page("test")
        page = AnswerPage(portal_topic=[topic])
        context = page.get_context(self.request)
        self.assertEqual(context["portal_page"], portal_page)

    def test_portal_page_no_primary_topic_multiple_portal_topics(self):
        topic1, portal_page1 = self.make_portal_topic_and_page("test1")
        topic2, portal_page2 = self.make_portal_topic_and_page("test2")
        page = AnswerPage(portal_topic=[topic1, topic2])
        context = page.get_context(self.request)
        self.assertIsNone(context["portal_page"])
