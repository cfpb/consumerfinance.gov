import json
import unittest

from django.apps import apps
from django.http import Http404, HttpRequest, QueryDict
from django.test import TestCase
from django.urls import NoReverseMatch, reverse
from django.utils import timezone

from wagtail.core.models import Site
from wagtailsharing.models import SharingSite

import mock
from model_bakery import baker

from ask_cfpb.documents import AnswerPageDocument, make_safe
from ask_cfpb.models import (
    ENGLISH_PARENT_SLUG, SPANISH_PARENT_SLUG, AnswerPage
)
from ask_cfpb.views import annotate_links, ask_search, redirect_ask_search
from v1.util.migrations import get_or_create_page


now = timezone.now()


class MockSearchResult:
    def __init__(self, app_label, model_name, pk, score, **kwargs):
        self.autocomplete = "What is mock question {}?".format(pk)
        self.url = "/ask-cfpb/mock-question-en-{}/".format(pk)
        self.text = "Mock answer text for question {}.".format(pk)
        self.preview = "Mock preview ..."


def mock_es7_queryset(count=0):
    class MockSearchQuerySet(AnswerPageDocument):
        def __iter__(self):
            if count:
                return iter(
                    [
                        MockSearchResult("ask_cfpb", "AnswerPage", i, 0.5)
                        for i in list(range(1, count + 1))
                    ]
                )
            else:
                return iter([])

        def count(self):
            return count

        def filter(self, *args, **kwargs):
            return self

        def models(self, *models):
            return self

    return MockSearchQuerySet()


class AskSearchSafetyCase(unittest.TestCase):
    def test_make_safe(self):
        test_phrase = "Would you like green eggs and ^~`[]#<>;|%\\{\\}\\?"
        self.assertEqual(
            make_safe(test_phrase), "Would you like green eggs and ?"
        )


class AnswerPagePreviewCase(TestCase):
    def setUp(self):
        from ask_cfpb.models import Answer
        from v1.models import HomePage

        self.root_page = HomePage.objects.get(slug="cfgov")
        self.english_parent_page = get_or_create_page(
            apps,
            "ask_cfpb",
            "AnswerLandingPage",
            "Ask CFPB",
            ENGLISH_PARENT_SLUG,
            self.root_page,
            language="en",
            live=True,
        )
        self.spanish_parent_page = get_or_create_page(
            apps,
            "ask_cfpb",
            "AnswerLandingPage",
            "Obtener respuestas",
            SPANISH_PARENT_SLUG,
            self.root_page,
            language="es",
            live=True,
        )
        self.test_answer = baker.make(Answer)
        self.test_answer2 = baker.make(Answer)
        self.english_answer_page = AnswerPage(
            answer_base=self.test_answer,
            language="en",
            slug="test-question1-en-{}".format(self.test_answer.pk),
            title="Test question1",
            answer_content="Test answer1.",
            question="Test question1.",
        )
        self.english_parent_page.add_child(instance=self.english_answer_page)
        self.english_answer_page.save_revision().publish()
        self.english_answer_page2 = AnswerPage(
            answer_base=self.test_answer2,
            language="en",
            slug="test-question2-en-{}".format(self.test_answer2.pk),
            title="Test question2",
            answer_content="Test answer2.",
            question="Test question2.",
        )
        self.english_parent_page.add_child(instance=self.english_answer_page2)
        self.english_answer_page2.save_revision().publish()
        self.site = baker.make(
            Site,
            root_page=self.root_page,
            hostname="localhost",
            port=8000,
            is_default_site=True,
        )
        self.sharing_site = baker.make(
            SharingSite,
            site=self.site,
            hostname="preview.localhost",
            port=8000,
        )

    @mock.patch("ask_cfpb.views.ServeView.serve")
    def test_preview_page(self, mock_serve):
        from ask_cfpb.views import view_answer

        test_request = HttpRequest()
        test_request.META["SERVER_NAME"] = "preview.localhost"
        test_request.META["SERVER_PORT"] = 8000
        view_answer(test_request, "test-question1", "en", self.test_answer.pk)
        self.assertEqual(mock_serve.call_count, 1)

    def test_answer_page_not_live(self):
        from ask_cfpb.views import view_answer

        page = self.test_answer.english_page
        page.unpublish()
        test_request = HttpRequest()
        with self.assertRaises(Http404):
            view_answer(
                test_request, "test-question", "en", self.test_answer.pk
            )

    def test_page_redirected(self):
        page = self.english_answer_page
        page.get_latest_revision().publish()
        page.redirect_to_page = self.english_answer_page2
        page.save()
        page.save_revision().publish()
        response = self.client.get(page.url)
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.url, self.english_answer_page2.url)


class AnswerViewTestCase(TestCase):
    def setUp(self):
        from v1.models import HomePage

        self.root_page = HomePage.objects.get(slug="cfgov")
        self.english_parent_page = get_or_create_page(
            apps,
            "ask_cfpb",
            "AnswerLandingPage",
            "Ask CFPB",
            ENGLISH_PARENT_SLUG,
            self.root_page,
            language="en",
            live=True,
        )
        self.spanish_parent_page = get_or_create_page(
            apps,
            "ask_cfpb",
            "AnswerLandingPage",
            "Obtener respuestas",
            SPANISH_PARENT_SLUG,
            self.root_page,
            language="es",
            live=True,
        )

    def test_annotate_links(self):
        mock_answer = (
            '<p>Answer with a <a href="http://fake.com">fake link.</a></p>'
        )
        (annotated_answer, links) = annotate_links(mock_answer)
        self.assertEqual(
            annotated_answer,
            '<html><body><p>Answer with a <a href="http://fake.com">fake '
            "link.</a><sup>1</sup></p></body></html>",
        )
        self.assertEqual(links, [(1, str("http://fake.com"))])

    def test_annotate_links_no_href(self):
        mock_answer = "<p>Answer with a <a>fake link.</a></p>"
        (annotated_answer, links) = annotate_links(mock_answer)
        self.assertEqual(links, [])

    def test_annotate_links_no_site(self):
        site = Site.objects.get(is_default_site=True)
        site.is_default_site = False
        site.save()
        with self.assertRaises(RuntimeError) as context:
            annotate_links("answer")
        self.assertIn("no default wagtail site", str(context.exception))

    def test_bad_language_search(self):
        with self.assertRaises(NoReverseMatch):
            self.client.get(
                reverse("ask-search-en", kwargs={"language": "zz"}),
                {"q": "payday"},
            )

    def test_en_search_results_page_not_created(self):
        response = self.client.get(reverse("ask-search-en"), {"q": "payday"})
        self.assertEqual(response.status_code, 404)

    @mock.patch("ask_cfpb.views.AnswerPageDocument.search")
    def test_en_search(self, mock_ask_search):
        from v1.util.migrations import get_or_create_page

        mock_page = get_or_create_page(
            apps,
            "ask_cfpb",
            "AnswerResultsPage",
            "Mock results page",
            "ask-cfpb-search-results",
            self.root_page,
            language="en",
        )

        mock_ask_search.queryset = mock_es7_queryset(count=3)
        mock_ask_search.suggestion = None
        mock_ask_search.search_term = "payday"
        response = self.client.get(reverse("ask-search-en"), {"q": "payday"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data["page"], mock_page)
        self.assertEqual(mock_ask_search.call_count, 1)
        self.assertTrue(
            mock_ask_search.called_with(language="en", search_term="payday")
        )

    @mock.patch("ask_cfpb.views.AnswerPageDocument.search")
    def test_en_search_no_term(self, mock_ask_search):
        from v1.util.migrations import get_or_create_page

        mock_page = get_or_create_page(
            apps,
            "ask_cfpb",
            "AnswerResultsPage",
            "Mock results page",
            "ask-cfpb-search-results",
            self.root_page,
            language="en",
        )
        mock_ask_search.queryset = mock_es7_queryset()
        response = self.client.get(reverse("ask-search-en"), {"q": ""})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data["page"], mock_page)
        self.assertEqual(response.context_data["page"].query, "")
        self.assertEqual(response.context_data["page"].result_query, "")

    # @override_settings(FLAGS={"ASK_SEARCH_TYPOS": [("boolean", True)]})
    # @mock.patch("ask_cfpb.views.AnswerPageSearch")
    # def test_en_search_suggestion(self, mock_search):
    #     from v1.util.migrations import get_or_create_page

    #     mock_page = get_or_create_page(
    #         apps,
    #         "ask_cfpb",
    #         "AnswerResultsPage",
    #         "Mock results page",
    #         "ask-cfpb-search-results",
    #         self.english_parent_page,
    #         language="en",
    #         live=True,
    #     )

    #     # AskSearch.sugggest flips search_term and suggestion when called
    #     mock_search.return_value = {
    #         'search_term': "paydya",
    #         'suggestion': "payday",
    #         'results': []
    #     }
    #     response = self.client.get(reverse("ask-search-en"), {"q": "paydya"})
    #     self.assertEqual(response.status_code, 200)
    #     response_page = response.context_data["page"]
    #     self.assertEqual(response_page, mock_page)
    #     self.assertEqual(response_page.result_query, "paydya")

    @mock.patch("ask_cfpb.views.redirect_ask_search")
    def test_ask_search_encounters_facets(self, mock_redirect):
        request = HttpRequest()
        request.GET["selected_facets"] = "category_exact:my_category"
        ask_search(request)
        self.assertEqual(mock_redirect.call_count, 1)

    @mock.patch("ask_cfpb.views.redirect")
    def test_redirect_ask_search_passes_query_string(self, mock_redirect):
        request = HttpRequest()
        request.GET["q"] = "hoodoo"
        redirect_ask_search(request)
        self.assertEqual(mock_redirect.call_count, 1)

    @mock.patch("ask_cfpb.views.redirect")
    def test_spanish_redirect_ask_search_passes_query_string(
        self, mock_redirect
    ):
        request = HttpRequest()
        request.GET["selected_facets"] = "category_exact:my_categoria"
        redirect_ask_search(request, language="es")
        self.assertEqual(mock_redirect.call_count, 1)

    @mock.patch("ask_cfpb.views.AnswerPageSearch")
    def test_es_search(self, mock_ask_search):
        get_or_create_page(
            apps,
            "ask_cfpb",
            "AnswerResultsPage",
            "Mock Spanish results page",
            "respuestas",
            self.spanish_parent_page,
            language="es",
            live=True,
        )
        mock_ask_search.queryset = mock_es7_queryset(count=1)
        mock_ask_search.suggestion = None
        mock_ask_search.search_term = "payday"
        self.client.get(
            reverse("ask-search-es", kwargs={"language": "es"}),
            {"q": "payday"},
        )
        self.assertEqual(mock_ask_search.call_count, 1)
        self.assertTrue(
            mock_ask_search.called_with(language="es", search_term="payday")
        )

    @mock.patch("ask_cfpb.views.AnswerPageSearch")
    def test_search_page_en_selection(self, mock_search):
        get_or_create_page(
            apps,
            "ask_cfpb",
            "AnswerResultsPage",
            "Mock results page",
            "ask-cfpb-search-results",
            self.english_parent_page,
            language="en",
            live=True,
        )
        mock_search.serch_term = "tuition"
        mock_search.queryset = mock_es7_queryset(count=1)
        response = self.client.get(reverse("ask-search-en"), {"q": "tuition"})
        self.assertEqual(mock_search.call_count, 1)
        self.assertEqual(response.context_data.get("page").language, "en")

    @mock.patch("ask_cfpb.views.AnswerPageSearch")
    def test_search_page_es_selection(self, mock_search):
        get_or_create_page(
            apps,
            "ask_cfpb",
            "AnswerResultsPage",
            "Mock Spanish results page",
            "respuestas",
            self.spanish_parent_page,
            language="es",
            live=True,
        )
        mock_search.serch_term = "hipotecas"
        mock_search.queryset = mock_es7_queryset(count=5)
        response = self.client.get(
            reverse("ask-search-es", kwargs={"language": "es"}),
            {"q": "hipotecas"},
        )
        self.assertEqual(mock_search.call_count, 1)
        self.assertEqual(response.context_data["page"].language, "es")

    # @mock.patch("ask_cfpb.views.AnswerPageSearch")
    # def test_json_response(self, mock_search):
    #     get_or_create_page(
    #         apps,
    #         "ask_cfpb",
    #         "AnswerResultsPage",
    #         "Mock results page",
    #         "ask-cfpb-search-results",
    #         self.english_parent_page,
    #         language="en",
    #         live=True,
    #     )
    #     mock_search.search.return_value = {
    #         'search_term': "tooition",
    #         'suggestion': None,
    #         'results': []
    #     }
    #     mock_search.suggest.return_value = {
    #         'search_term': "tooition",
    #         'suggestion': "tuition",
    #         'results': []
    #     }
    #     response = self.client.get(
    #         reverse("ask-search-en-json", kwargs={"as_json": "json"}),
    #         {"q": "tuition"},
    #     )
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(mock_search.call_count, 1)
    #     self.assertEqual(json.loads(response.content)["query"], "tooition")

    # @mock.patch("ask_cfpb.views.AnswerPageSearch")
    # def test_autocomplete_en_blank_term(self, mock_search):
    #     result = self.client.get(reverse("ask-autocomplete-en"), {"term": ""})  # noqa
    #     output = json.loads(result.content)
    #     self.assertEqual(output, [])

    @mock.patch("ask_cfpb.views.AnswerPageSearch")
    def test_autocomplete_es_blank_term(self, mock_search):
        result = self.client.get(
            reverse("ask-autocomplete-es", kwargs={"language": "es"}),
            {"term": ""},
        )
        output = json.loads(result.content)
        self.assertEqual(output, [])

    # @mock.patch("ask_cfpb.views.AnswerPageSearch")
    # def test_autocomplete_en(self, mock_search):
    #     mock_search_result = mock.Mock()
    #     mock_search_result.autocomplete = "question"
    #     mock_search_result.url = "url"
    #     mock_search.execute.return_value = [mock_search_result]
    #     self.client.get(
    #         reverse("ask-autocomplete-en"), {"term": "question"}
    #     )
    #     self.assertEqual(mock_search.call_count, 1)

    @mock.patch("ask_cfpb.views.AnswerPageDocument.search")
    def test_autocomplete_espaniol(self, mock_autocomplete):
        mock_search_result = mock.Mock()
        mock_search_result.autocomplete = "Spanish question"
        mock_search_result.url = "respuestas/url"
        mock_autocomplete.query.return_value = [mock_search_result]
        result = self.client.get(
            reverse("ask-autocomplete-es", kwargs={"language": "es"}),
            {"term": "question"},
        )
        self.assertEqual(mock_autocomplete.call_count, 1)
        self.assertEqual(result.status_code, 200)


class RedirectAskSearchTestCase(TestCase):
    def test_redirect_search_no_facets(self):
        request = HttpRequest()
        result = redirect_ask_search(request)
        self.assertEqual(result.get("location"), "/ask-cfpb/search/")

    def test_redirect_search_blank_facets(self):
        request = HttpRequest()
        request.GET["selected_facets"] = ""
        result = redirect_ask_search(request)
        self.assertEqual(result.get("location"), "/ask-cfpb/search/")

    def test_redirect_search_uppercase_facet(self):
        """Handle odd requests with uppercase, spaced category names."""
        category_querystring = "selected_facets=category_exact:Prepaid Cards"
        request = HttpRequest()
        request.GET = QueryDict(category_querystring)
        result = redirect_ask_search(request)
        self.assertEqual(
            result.get("location"), "/ask-cfpb/category-prepaid-cards/"
        )

    def test_redirect_search_no_query(self):
        request = HttpRequest()
        request.GET["q"] = " "
        result = redirect_ask_search(request)
        self.assertEqual(result.get("location"), "/ask-cfpb/search/")

    def test_redirect_search_with_category(self):
        category_querystring = (
            "selected_facets=category_exact:my_category"
            "&selected_facets=category_exact:my_category2"
            "&selected_facets=audience_exact:Older+Americans"
            "&selected_facets=audience_exact:my_audience2"
            "&selected_facets=tag_exact:mytag1"
            "&selected_facets=tag_exact:mytag2"
        )
        request = HttpRequest()
        request.GET = QueryDict(category_querystring)
        result = redirect_ask_search(request)
        self.assertEqual(
            result.get("location"), "/ask-cfpb/category-my_category/"
        )

    def test_redirect_search_with_audience(self):
        audience_querystring = (
            "selected_facets=audience_exact:Older+Americans"
            "&selected_facets=audience_exact:my_audience2"
        )
        request = HttpRequest()
        request.GET = QueryDict(audience_querystring)
        result = redirect_ask_search(request)
        self.assertEqual(
            result.get("location"), "/ask-cfpb/audience-older-americans/"
        )

    def test_spanish_redirect_search_with_tag(self):
        target_tag = "spanishtag1"
        tag_querystring = (
            "selected_facets=tag_exact:{}"
            "&selected_facets=tag_exact:spanishtag2".format(target_tag)
        )
        request = HttpRequest()
        request.GET = QueryDict(tag_querystring)
        result = redirect_ask_search(request, language="es")
        self.assertEqual(
            result.get("location"),
            "/es/obtener-respuestas/buscar-por-etiqueta/{}/".format(
                target_tag
            ),
        )

    def test_english_redirect_search_with_tag(self):
        target_tag = "englishtag1"
        tag_querystring = (
            "selected_facets=tag_exact:{}"
            "&selected_facets=tag_exact:englishtag2".format(target_tag)
        )
        request = HttpRequest()
        request.GET = QueryDict(tag_querystring)
        result = redirect_ask_search(request, language="en")
        self.assertEqual(
            result.get("location"),
            "/ask-cfpb/search-by-tag/{}/".format(target_tag),
        )

    def test_redirect_search_with_unrecognized_facet_raises_404(self):
        querystring = (
            "sort=-updated_at&selected_facets=imtkfidycqszgfdb&page=60"
        )
        request = HttpRequest()
        request.GET = QueryDict(querystring)
        with self.assertRaises(Http404):
            redirect_ask_search(request)
