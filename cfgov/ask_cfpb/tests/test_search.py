import json
import unittest
from io import StringIO
from unittest import mock

from django.test import TestCase

from opensearchpy.exceptions import RequestError

from ask_cfpb.documents import AnswerPageDocument
from ask_cfpb.forms import AutocompleteForm
from ask_cfpb.models.answer_page import AnswerPage
from ask_cfpb.models.django import Answer
from ask_cfpb.models.search import (
    UNSAFE_CHARACTERS,
    AnswerPageSearch,
    make_safe,
)
from search.elasticsearch_helpers import ElasticsearchTestsMixin


def make_answer():
    test_answer = Answer()
    test_answer.save()
    return test_answer


class TestSearchMakeSafe(unittest.TestCase):
    def test_make_safe(self):
        term = "What is a mortgage"
        unsafe_term = term + "".join(UNSAFE_CHARACTERS)
        self.assertEqual(term, make_safe(unsafe_term))


class TestAnswerPageSearch(ElasticsearchTestsMixin, TestCase):
    def setUp(self):
        from v1.models import HomePage

        self.ROOT_PAGE = HomePage.objects.get(slug="cfgov")

    def test_AnswerPageSearch_init_en(self):
        search_term = "tax"
        english_answerPage = AnswerPageSearch(search_term=search_term)
        self.assertEqual(english_answerPage.language, "en")
        self.assertEqual(english_answerPage.search_term, search_term)
        self.assertIsNone(english_answerPage.base_query)
        self.assertIsNone(english_answerPage.suggestion)
        self.assertEqual(english_answerPage.results, [])

    def test_AnswerPageSearch_init_es(self):
        search_term = "impuesto"
        spanish_answerPage = AnswerPageSearch(
            search_term=search_term, language="es"
        )
        self.assertEqual(spanish_answerPage.language, "es")
        self.assertEqual(spanish_answerPage.search_term, search_term)
        self.assertIsNone(spanish_answerPage.base_query)
        self.assertIsNone(spanish_answerPage.suggestion)
        self.assertEqual(spanish_answerPage.results, [])

    def test_AnswerPageSearch_autocomplete(self):
        test_answer_page = AnswerPage(
            title="Money 101",
            question="What is money?",
            slug="test-answer-page",
            live=True,
            answer_base=make_answer(),
        )
        self.ROOT_PAGE.add_child(instance=test_answer_page)
        self.rebuild_elasticsearch_index(
            AnswerPageDocument.Index.name, stdout=StringIO()
        )
        search_term = "mone"
        test_answer_page_search = AnswerPageSearch(search_term=search_term)
        self.assertEqual(
            test_answer_page_search.autocomplete()[0]["question"],
            "What is money?",
        )

    def test_AnswerPageSearch_autocomplete_error(self):
        with mock.patch(
            "ask_cfpb.documents.AnswerPageDocument.search",
            side_effect=RequestError,
        ):
            results = AnswerPageSearch.autocomplete("mone")
            self.assertEqual(results, [])

    def test_AnswerPage_search(self):
        test_answer_page = AnswerPage(
            title="Money 101",
            question="What is money?",
            answer_content=json.dumps(
                [
                    {
                        "type": "text",
                        "value": {
                            "anchor_tag": "",
                            "content": "Money makes the world go round.",
                        },
                    }
                ]
            ),
            slug="test-answer-page",
            live=True,
            answer_base=make_answer(),
        )
        self.ROOT_PAGE.add_child(instance=test_answer_page)
        self.rebuild_elasticsearch_index(
            AnswerPageDocument.Index.name, stdout=StringIO()
        )
        search_term = "What is money?"
        test_answer_page_search = AnswerPageSearch(search_term=search_term)
        test_answer_page_search_results = test_answer_page_search.search()[
            "results"
        ][0].text.rstrip()
        self.assertEqual(
            test_answer_page_search_results,
            "What is money?\nMoney makes the world go round.",
        )

    def test_answerpage_search_default_id_sort_order(self):
        for page in [
            AnswerPage(
                **{k: f"test-{letter}" for k in ("title", "slug", "question")},
                live=True,
                answer_base=make_answer(),
            )
            for letter in "abc"
        ]:
            self.ROOT_PAGE.add_child(instance=page)

        self.rebuild_elasticsearch_index(
            AnswerPageDocument.Index.name, stdout=StringIO()
        )

        results = AnswerPageSearch("test").search()
        ordered_ids = list(
            [
                str(answer_page_document.answer_id)
                for answer_page_document in results["results"]
            ]
        )
        sorted_ids = list(ordered_ids)
        sorted_ids.sort()

        self.assertEqual(ordered_ids, sorted_ids)

    def test_AnswerPage_suggest(self):
        test_answer_page = AnswerPage(
            title="Money 101",
            question="What is money?",
            answer_content=json.dumps(
                [
                    {
                        "type": "text",
                        "value": {
                            "anchor_tag": "",
                            "content": "Money makes the world go round.",
                        },
                    }
                ]
            ),
            slug="test-answer-page3",
            live=True,
            answer_base=make_answer(),
        )
        self.ROOT_PAGE.add_child(instance=test_answer_page)
        self.rebuild_elasticsearch_index(
            AnswerPageDocument.Index.name, stdout=StringIO()
        )
        search_term = "monye"
        test_answer_page_search = AnswerPageSearch(search_term=search_term)
        test_answer_page_search_results = test_answer_page_search.suggest()
        self.assertEqual(
            test_answer_page_search_results["search_term"], "money"
        )

    def test_AnswerPage_suggest_error(self):
        with mock.patch(
            "ask_cfpb.documents.AnswerPageDocument.search"
        ) as mock_search:
            # break-up for line length
            mock_filter = mock_search.return_value.filter.return_value
            mock_execute = (
                mock_filter.suggest.return_value.execute.return_value
            )
            mock_execute.suggest.suggestion = []
            result = AnswerPageSearch(search_term="money").suggest()
            self.assertIsNone(result["suggestion"])

    @mock.patch("ask_cfpb.forms.AutocompleteForm")
    def test_ask_search_autocomplete_honors_max_chars(self, mock_query):
        valid_term_1 = "Here is an ask_cfpb query that is exactly,"
        valid_term_2 = " like 100 percent, 75 characters."
        overage = " This is overage text that should not appear in the query"
        too_long_term = valid_term_1 + valid_term_2 + overage
        mock_query.cleaned_data = {"term": too_long_term}
        self.assertEqual(
            valid_term_1 + valid_term_2,
            AutocompleteForm.clean_term(mock_query),
        )
