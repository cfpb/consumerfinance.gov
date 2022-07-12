import json
import pdb
import unittest
import json
from unittest import mock
from ask_cfpb.models.answer_page import AnswerPage

from django_elasticsearch_dsl.registries import DocumentRegistry, registry
from django.apps import apps
from django.http import Http404, HttpRequest, QueryDict
from django.test import TestCase, override_settings
from django.urls import reverse
from ask_cfpb.forms import AutocompleteForm
from ask_cfpb.models.search import UNSAFE_CHARACTERS

from elasticsearch.exceptions import RequestError

from ask_cfpb.documents import AnswerPageDocument
from ask_cfpb.models import ENGLISH_PARENT_SLUG, SPANISH_PARENT_SLUG
from ask_cfpb.models.search import AnswerPageSearch, make_safe
from ask_cfpb.views import ask_search, redirect_ask_search
from v1.util.migrations import get_or_create_page

class TestSearchMakeSafe(unittest.TestCase):

    def test_make_safe(self):
        term = 'What is a mortgage'
        unsafe_term = term + ''.join(UNSAFE_CHARACTERS)
        self.assertEqual(term, make_safe(unsafe_term))




class TestAnswerPageSearch(unittest.TestCase):

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
    
    def test_AnswerPageSearch_init_en(self):
        search_term = 'tax'
        english_answerPage = AnswerPageSearch(search_term=search_term)
        assert english_answerPage.language == 'en'
        assert english_answerPage.search_term == search_term
        assert english_answerPage.base_query == None
        assert english_answerPage.suggestion == None
        assert english_answerPage.results == []


    def test_AnswerPageSearch_init_es(self):
        search_term = 'impuesto'
        spanish_answerPage = AnswerPageSearch(search_term=search_term, language='es')
        assert spanish_answerPage.language == 'es'
        assert spanish_answerPage.search_term == search_term
        assert spanish_answerPage.base_query == None
        assert spanish_answerPage.suggestion == None
        assert spanish_answerPage.results == []


    def test_AnswerPageSearch_autocomplete_en(self):
        test_answer_page = AnswerPage(title="Hello", question="Hello?", slug="/test-answer-page")
        test_answer_page.save()
        test_answer_page.get_latest_revision().publish()
        registry.update(test_answer_page)
        # print('printttt')
        # print(test_answer_page.search()
        #         .filter("term", language=self.language)
        #         .query(
        #             "match",
        #             autocomplete="hello",
        #         ))
        search_term = "hell"
        test_answer_page_search = AnswerPageSearch(search_term=search_term)
        self.assertEqual(test_answer_page_search.autocomplete(), "hello")
