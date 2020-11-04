import json
import unittest

from django.apps import apps
from django.http import Http404, HttpRequest, QueryDict
from django.test import TestCase, override_settings
from django.urls import NoReverseMatch, reverse

import mock

from ask_cfpb.documents import AnswerPageDocument
from ask_cfpb.models import ENGLISH_PARENT_SLUG, SPANISH_PARENT_SLUG
from ask_cfpb.models.search import AnswerPageSearch, SearchQuerySet, make_safe
from ask_cfpb.tests.models.test_pages import mock_queryset
from ask_cfpb.views import ask_search, redirect_ask_search
from v1.util.migrations import get_or_create_page


class AskSearchSafetyTestCase(unittest.TestCase):
    def test_make_safe(self):
        test_phrase = "Would you like green eggs and ^~`[]#<>;|%\\{\\}\\?"
        self.assertEqual(
            make_safe(test_phrase), "Would you like green eggs and ?"
        )


class AskSearchTestCase(TestCase):
    def test_en_search_results_page_not_created(self):
        response = self.client.get(reverse("ask-search-en"), {"q": "payday"})
        self.assertEqual(response.status_code, 404)


class AskSearchTest(TestCase):
    def setUp(self):
        from v1.models import HomePage

        self.ROOT_PAGE = HomePage.objects.get(slug="cfgov")
        self.english_parent_page = get_or_create_page(
            apps,
            "ask_cfpb",
            "AnswerLandingPage",
            "Ask CFPB",
            ENGLISH_PARENT_SLUG,
            self.ROOT_PAGE,
            language="en",
            live=True,
        )
        self.spanish_parent_page = get_or_create_page(
            apps,
            "ask_cfpb",
            "AnswerLandingPage",
            "Obtener respuestas",
            SPANISH_PARENT_SLUG,
            self.ROOT_PAGE,
            language="es",
            live=True,
        )
        self.en_page = get_or_create_page(
            apps,
            "ask_cfpb",
            "AnswerResultsPage",
            "Mock results page",
            "ask-cfpb-search-results",
            self.english_parent_page,
            language="en",
            live=True,
        )
        self.es_page = get_or_create_page(
            apps,
            "ask_cfpb",
            "AnswerResultsPage",
            "Mock Spanish results page",
            "respuestas",
            self.spanish_parent_page,
            language="es",
            live=True,
        )

    def test_bad_language_search(self):
        with self.assertRaises(NoReverseMatch):
            self.client.get(
                reverse("ask-search-en", kwargs={"language": "zz"}),
                {"q": "payday"},
            )

    @mock.patch("ask_cfpb.views.AskSearch")
    def test_en_search(self, mock_ask_search):
        mock_ask_search.queryset = mock_queryset(count=3)
        mock_ask_search.suggestion = None
        mock_ask_search.search_term = "payday"
        response = self.client.get(reverse("ask-search-en"), {"q": "payday"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data["page"], self.en_page)
        self.assertEqual(mock_ask_search.call_count, 1)
        self.assertTrue(
            mock_ask_search.called_with(language="en", search_term="payday")
        )

    @mock.patch("ask_cfpb.views.AskSearch")
    def test_en_search_no_term(self, mock_ask_search):
        mock_ask_search.queryset = mock_queryset()
        response = self.client.get(reverse("ask-search-en"), {"q": ""})
        self.assertEqual(response.status_code, 200)
        response_page = response.context_data["page"]
        self.assertEqual(response_page, self.en_page)
        self.assertEqual(response_page.query, "")
        self.assertEqual(response_page.result_query, "")

    @override_settings(FLAGS={"ASK_SEARCH_TYPOS": [("boolean", True)]})
    @mock.patch.object(SearchQuerySet, 'spelling_suggestion')
    @mock.patch.object(SearchQuerySet, 'filter')
    def test_en_search_suggestion(self, mock_filter, mock_search):
        # AskSearch.suggest flips search_term and suggestion when called
        mock_filter.return_value = mock_queryset(count=0)
        mock_search.return_value = "payday"
        response = self.client.get(reverse("ask-search-en"), {"q": "paydya"})
        self.assertEqual(response.status_code, 200)
        response_page = response.context_data["page"]
        self.assertEqual(response_page, self.en_page)
        self.assertEqual(response_page.result_query, "payday")
        self.assertEqual(response_page.query, "paydya")

    @mock.patch("ask_cfpb.views.AskSearch")
    def test_es_search(self, mock_ask_search):
        mock_ask_search.queryset = mock_queryset(count=1)
        mock_ask_search.suggestion = None
        mock_ask_search.search_term = "payday"
        response = self.client.get(
            reverse("ask-search-es", kwargs={"language": "es"}),
            {"q": "payday"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data["page"], self.es_page)
        self.assertEqual(mock_ask_search.call_count, 1)
        self.assertTrue(
            mock_ask_search.called_with(language="es", search_term="payday")
        )

    @mock.patch("ask_cfpb.views.AskSearch")
    def test_search_page_en_selection(self, mock_search):
        mock_search.search_term = "tuition"
        mock_search.queryset = mock_queryset(count=1)
        response = self.client.get(reverse("ask-search-en"), {"q": "tuition"})
        self.assertEqual(mock_search.call_count, 1)
        self.assertEqual(response.context_data.get("page").language, "en")
        self.assertEqual(
            self.en_page.get_template(HttpRequest()),
            "ask-cfpb/answer-search-results.html",
        )

    @mock.patch("ask_cfpb.views.AskSearch")
    def test_search_page_es_selection(self, mock_search):
        mock_search.search_term = "hipotecas"
        mock_search.queryset = mock_queryset(count=5)
        response = self.client.get(
            reverse("ask-search-es", kwargs={"language": "es"}),
            {"q": "hipotecas"},
        )
        self.assertEqual(self.es_page.answers, [])
        self.assertEqual(mock_search.call_count, 1)
        self.assertEqual(response.context_data["page"].language, "es")
        self.assertEqual(
            self.es_page.get_template(HttpRequest()),
            "ask-cfpb/answer-search-results.html",
        )

    @mock.patch.object(SearchQuerySet, 'spelling_suggestion')
    @mock.patch.object(SearchQuerySet, 'filter')
    def test_json_response(self, mock_filter, mock_search):
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
        mock_search.return_value = "tuition"
        mock_filter.count.return_value = 5
        mock_filter.return_value = mock_queryset(count=5)
        response = self.client.get(
            reverse("ask-search-en-json", kwargs={"as_json": "json"}),
            {"q": "tuition"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_filter.call_count, 1)
        self.assertEqual(json.loads(response.content)["query"], "tuition")

    def test_autocomplete_en_blank_term(self):
        result = self.client.get(reverse("ask-autocomplete-en"), {"term": ""})
        self.assertEqual(json.loads(result.content), [])

    def test_autocomplete_es_blank_term(self):
        result = self.client.get(
            reverse("ask-autocomplete-es", kwargs={"language": "es"}),
            {"term": ""},
        )
        self.assertEqual(json.loads(result.content), [])

    @mock.patch.object(SearchQuerySet, 'autocomplete')
    def test_autocomplete_en(self, mock_autocomplete):
        mock_search_result = mock.Mock()
        mock_search_result.autocomplete = "question"
        mock_search_result.url = "url"
        mock_autocomplete.return_value = [mock_search_result]
        result = self.client.get(
            reverse("ask-autocomplete-en"), {"term": "question"}
        )
        self.assertEqual(mock_autocomplete.call_count, 1)
        output = json.loads(result.content)
        self.assertEqual(sorted(output[0].keys()), ["question", "url"])

    @mock.patch.object(SearchQuerySet, 'autocomplete')
    def test_autocomplete_es(self, mock_autocomplete):
        mock_search_result = mock.Mock()
        mock_search_result.autocomplete = "question"
        mock_search_result.url = "url"
        mock_autocomplete.return_value = [mock_search_result]
        result = self.client.get(
            reverse("ask-autocomplete-es", kwargs={"language": "es"}),
            {"term": "question"},
        )
        self.assertEqual(mock_autocomplete.call_count, 1)
        output = json.loads(result.content)
        self.assertEqual(sorted(output[0].keys()), ["question", "url"])


class AnswerPageSearchTest(TestCase):
    def setUp(self):
        from v1.models import HomePage

        self.ROOT_PAGE = HomePage.objects.get(slug="cfgov")
        self.english_parent_page = get_or_create_page(
            apps,
            "ask_cfpb",
            "AnswerLandingPage",
            "Ask CFPB",
            ENGLISH_PARENT_SLUG,
            self.ROOT_PAGE,
            language="en",
            live=True,
        )
        self.spanish_parent_page = get_or_create_page(
            apps,
            "ask_cfpb",
            "AnswerLandingPage",
            "Obtener respuestas",
            SPANISH_PARENT_SLUG,
            self.ROOT_PAGE,
            language="es",
            live=True,
        )
        self.en_page = get_or_create_page(
            apps,
            "ask_cfpb",
            "AnswerResultsPage",
            "Mock English results page",
            "ask-cfpb-search-results",
            self.english_parent_page,
            language="en",
            live=True,
        )
        self.es_page = get_or_create_page(
            apps,
            "ask_cfpb",
            "AnswerResultsPage",
            "Mock Spanish results page",
            "respuestas",
            self.spanish_parent_page,
            language="es",
            live=True,
        )

    @override_settings(FLAGS={"ELASTICSEARCH_DSL_ASK": [("boolean", True)]})
    @mock.patch.object(AnswerPageDocument, 'search')
    def test_en_search_es7(self, mock_search):
        term = "payday"
        mock_return = mock.Mock()
        mock_return.search_term = term
        mock_return.suggestion = None
        mock_es_queryset = mock.Mock()
        mock_es_queryset.__iter__ = mock.Mock(return_value=iter([mock_return]))
        mock_es_queryset.count.return_value = 3
        response = self.client.get(reverse("ask-search-en"), {"q": term})
        mock_search().query().filter() \
            .__getitem__().execute.return_value = [mock_return]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data["page"], self.en_page)
        self.assertEqual(mock_search.call_count, 2)
        self.assertTrue(
            mock_search.called_with(language="en", search_term=term)
        )

    @override_settings(FLAGS={"ELASTICSEARCH_DSL_ASK": [("boolean", True)]})
    @mock.patch.object(AnswerPageDocument, 'search')
    def test_en_search_es7_no_term(self, mock_search):
        term = ""
        mock_return = mock.Mock()
        mock_return.search_term = term
        mock_es_queryset = mock.Mock()
        mock_es_queryset.__iter__ = mock.Mock(return_value=iter([mock_return]))
        mock_es_queryset.count.return_value = 1
        response = self.client.get(reverse("ask-search-en"), {"q": term})
        self.assertEqual(mock_search.call_count, 0)
        self.assertEqual(response.status_code, 200)
        response_page = response.context_data["page"]
        self.assertEqual(response_page, self.en_page)
        self.assertEqual(response_page.query, term)
        self.assertEqual(response_page.result_query, term)

    @override_settings(FLAGS={"ASK_SEARCH_TYPOS": [("boolean", True)]})
    @override_settings(FLAGS={"ELASTICSEARCH_DSL_ASK": [("boolean", True)]})
    @mock.patch.object(AnswerPageDocument, 'search')
    def test_en_search_suggestion_es7(self, mock_search):
        term = "paydya"
        mock_return = mock.Mock()
        mock_return.suggestion = "payday"
        mock_return.search_term = term
        mock_es_queryset = mock.Mock()
        mock_es_queryset.__iter__ = mock.Mock(return_value=iter([mock_return]))
        mock_es_queryset.count.return_value = 0
        mock_search().suggest().execute().suggest.suggestion \
            .__getitem__().execute.return_value = [mock_return]
        mock_count = mock.Mock(return_value=0)
        mock_search().suggest().count = mock_count
        mock_search().suggest().execute().suggest.suggestion \
            .__getitem__().count = mock_count
        response = self.client.get(reverse("ask-search-en"), {"q": term})
        self.assertEqual(mock_search.call_count, 4)
        self.assertEqual(response.status_code, 200)
        response_page = response.context_data["page"]
        self.assertEqual(response_page, self.en_page)
        self.assertEqual(response_page.query, term)
        self.assertEqual(response_page.result_query, term)
        self.assertEqual(response_page.suggestion, None)

    @override_settings(FLAGS={"ELASTICSEARCH_DSL_ASK": [("boolean", True)]})
    @mock.patch("ask_cfpb.views.AnswerPageSearch")
    def test_es_search_es7(self, mock_search):
        term = "payday"
        mock_return = mock.Mock()
        mock_return.search_term = term
        mock_return.suggestion = None
        mock_es_queryset = mock.Mock()
        mock_es_queryset.__iter__ = mock.Mock(return_value=iter([mock_return]))
        mock_es_queryset.count.return_value = 1
        mock_search().query().filter() \
            .__getitem__().execute.return_value = [mock_return]
        response = self.client.get(
            reverse("ask-search-es", kwargs={"language": "es"}),
            {"q": term},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data["page"], self.es_page)
        self.assertEqual(mock_search.call_count, 2)
        self.assertTrue(
            mock_search.called_with(language="es", search_term=term)
        )

    @override_settings(FLAGS={"ELASTICSEARCH_DSL_ASK": [("boolean", True)]})
    @mock.patch("ask_cfpb.views.AnswerPageSearch")
    def test_search_page_es7_en_selection(self, mock_search):
        term = "tuition"
        mock_return = mock.Mock()
        mock_return.search_term = term
        mock_es_queryset = mock.Mock()
        mock_es_queryset.__iter__ = mock.Mock(return_value=iter([mock_return]))
        mock_es_queryset.count.return_value = 1
        mock_search().query().filter() \
            .__getitem__().execute.return_value = [mock_return]
        mock_count = mock.Mock(return_value=1)
        mock_search().query().count = mock_count
        mock_search().query().filter().__getitem__().count = mock_count
        response = self.client.get(reverse("ask-search-en"), {"q": term})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_search.call_count, 4)
        self.assertEqual(response.context_data.get("page").language, "en")

    @override_settings(FLAGS={"ELASTICSEARCH_DSL_ASK": [("boolean", True)]})
    @mock.patch("ask_cfpb.views.AnswerPageSearch")
    def test_search_page_es7_es_selection(self, mock_search):
        term = "hipotecas"
        mock_return = mock.Mock()
        mock_return.search_term = term
        mock_es_queryset = mock.Mock()
        mock_es_queryset.__iter__ = mock.Mock(return_value=iter([mock_return]))
        mock_es_queryset.count.return_value = 5
        mock_search().query().filter() \
            .__getitem__().execute.return_value = [mock_return]
        mock_count = mock.Mock(return_value=5)
        mock_search().query().count = mock_count
        mock_search().query().filter().__getitem__().count = mock_count
        response = self.client.get(
            reverse("ask-search-es", kwargs={"language": "es"}),
            {"q": term},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_search.call_count, 4)
        self.assertEqual(response.context_data["page"].language, "es")

    @override_settings(FLAGS={"ELASTICSEARCH_DSL_ASK": [("boolean", True)]})
    @mock.patch("ask_cfpb.views.AnswerPageSearch")
    def test_json_response_es7(self, mock_search):
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
        mock_search.search.return_value = {
            'search_term': "tooition",
            'suggestion': None,
            'results': []
        }
        mock_search.suggest.return_value = {
            'search_term': "tooition",
            'suggestion': "tuition",
            'results': []
        }
        response = self.client.get(
            reverse("ask-search-en-json", kwargs={"as_json": "json"}),
            {"q": "tuition"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_search.call_count, 1)
        self.assertEqual(json.loads(response.content)["query"], "tuition")

    @override_settings(FLAGS={"ELASTICSEARCH_DSL_ASK": [("boolean", True)]})
    @mock.patch.object(AnswerPageSearch, 'autocomplete')
    def test_autocomplete_es7_en_blank_term(self, mock_autocomplete):
        result = self.client.get(reverse("ask-autocomplete-en"), {"term": ""})
        self.assertEqual(json.loads(result.content), [])

    @override_settings(FLAGS={"ELASTICSEARCH_DSL_ASK": [("boolean", True)]})
    @mock.patch.object(AnswerPageSearch, 'autocomplete')
    def test_autocomplete_es7_es_blank_term(self, mock_autocomplete):
        result = self.client.get(
            reverse("ask-autocomplete-es", kwargs={"language": "es"}),
            {"term": ""},
        )
        self.assertEqual(json.loads(result.content), [])

    @override_settings(FLAGS={"ELASTICSEARCH_DSL_ASK": [("boolean", True)]})
    @mock.patch.object(AnswerPageDocument, 'search')
    def test_autocomplete_es7_en(self, mock_autocomplete):
        mock_search_result = mock.Mock()
        mock_search_result.autocomplete = "question"
        mock_search_result.url = "url"
        mock_autocomplete.query.return_value = [mock_search_result]
        result = self.client.get(
            reverse("ask-autocomplete-en"), {"term": "question"}
        )
        self.assertEqual(mock_autocomplete.call_count, 1)
        self.assertEqual(result.status_code, 200)

    @override_settings(FLAGS={"ELASTICSEARCH_DSL_ASK": [("boolean", True)]})
    @mock.patch.object(AnswerPageDocument, 'search')
    def test_autocomplete_es7_es(self, mock_autocomplete):
        mock_search_result = mock.Mock()
        mock_search_result.autocomplete = "question"
        mock_search_result.url = "respuestas/url"
        mock_autocomplete.query.return_value = [mock_search_result]
        result = self.client.get(
            reverse("ask-autocomplete-es", kwargs={"language": "es"}),
            {"term": "question"},
        )
        self.assertEqual(mock_autocomplete.call_count, 1)
        self.assertEqual(result.status_code, 200)


class RedirectAskSearchTestCase(TestCase):
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
