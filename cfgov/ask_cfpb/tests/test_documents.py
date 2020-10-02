# Based on https://github.com/django-es/django-elasticsearch-dsl/blob/master/tests/test_documents.py  # noqa
from unittest import TestCase

from django.apps import apps
from django.db import models

from wagtail.core.models import Site

from django_elasticsearch_dsl import fields
from django_elasticsearch_dsl.documents import DocType
from django_elasticsearch_dsl.exceptions import ModelFieldNotMappedError
from mock import patch

from ask_cfpb.documents import AnswerPageDocument
from ask_cfpb.models import AnswerPage
from ask_cfpb.models.django import (
    ENGLISH_PARENT_SLUG, SPANISH_PARENT_SLUG, Answer
)
from v1.util.migrations import get_or_create_page


class AnswerPageDocumentTest(TestCase):

    def test_model_class_added(self):
        self.assertEqual(AnswerPageDocument.django.model, AnswerPage)

    def test_ignore_signal_default(self):
        self.assertFalse(AnswerPageDocument.django.ignore_signals)

    def test_auto_refresh_default(self):
        self.assertTrue(AnswerPageDocument.django.auto_refresh)

    def test_fields_populated(self):
        mapping = AnswerPageDocument._doc_type.mapping
        self.assertEqual(
            set(mapping.properties.properties.to_dict().keys()),
            set(
                [
                    'autocomplete', 'portal_categories', 'portal_topics',
                    'text', 'url', 'preview', 'search_tags', 'language'
                ]
            )
        )

    def test_to_field(self):
        doc = DocType()
        for f in ['question', 'statement']:
            nameField = doc.to_field(f, AnswerPage._meta.get_field(f))
            self.assertIsInstance(nameField, fields.TextField)
            self.assertEqual(nameField._path, [f])
        dateField = doc.to_field(
            'last_edited', AnswerPage._meta.get_field('last_edited')
        )
        self.assertIsInstance(dateField, fields.DateField)
        self.assertEqual(dateField._path, ['last_edited'])
        for f in ['featured', 'share_and_print']:
            boolField = doc.to_field(f, AnswerPage._meta.get_field(f))
            self.assertIsInstance(boolField, fields.BooleanField)
            self.assertEqual(boolField._path, [f])
        intField = doc.to_field(
            'featured_rank', AnswerPage._meta.get_field('featured_rank')
        )
        self.assertIsInstance(intField, fields.IntegerField)
        self.assertEqual(intField._path, ['featured_rank'])

    def test_to_field_with_unknown_field(self):
        doc = DocType()
        with self.assertRaises(ModelFieldNotMappedError):
            doc.to_field(
                'answer_base', AnswerPage._meta.get_field('answer_base')
            )

    def test_mapping(self):
        self.assertEqual(
            AnswerPageDocument._doc_type.mapping.to_dict(), {
                'properties': {
                    'autocomplete': {
                        'analyzer': 'label_autocomplete', 'type': 'text'
                    },
                    'language': {'type': 'text'},
                    'portal_categories': {'type': 'text'},
                    'portal_topics': {'type': 'keyword'},
                    'preview': {'type': 'text'},
                    'search_tags': {'type': 'text'},
                    'text': {
                        'analyzer': 'synonym_analyzer_en', 'type': 'text'
                    },
                    'url': {'type': 'text'}
                }
            }
        )

    def test_get_queryset(self):
        qs = AnswerPageDocument().get_queryset()
        self.assertIsInstance(qs, models.QuerySet)
        self.assertEqual(qs.model, AnswerPage)

    def test_prepare(self):
        self.site = Site.objects.get(is_default_site=True)
        self.english_parent_page = get_or_create_page(
            apps,
            "ask_cfpb",
            "AnswerLandingPage",
            "Ask CFPB",
            ENGLISH_PARENT_SLUG,
            self.site.root_page,
            language="en",
            live=True,
        )
        self.answer = Answer(id=1234)
        self.answer.save()
        self.page = AnswerPage(
            language="en",
            slug="mock-english-question-en-1234",
            title="Mock English question",
            answer_base=self.answer,
            answer_content="Mock English answer",
            question="Mock English question",
            search_tags="English",
        )
        self.english_parent_page.add_child(instance=self.page)
        self.page.save_revision().publish()
        doc = AnswerPageDocument()
        prepared_data = doc.prepare(self.page)
        self.assertEqual(
            prepared_data, {
                'autocomplete': doc.prepare_autocomplete(None),
                'portal_categories': doc.prepare_portal_categories(None),
                'portal_topics': doc.prepare_portal_topics(None),
                'url': doc.test_prepare_url(None),
                'search_tags': doc.prepare_search_tags(None),
                'language': 'en'
            }
        )

    def test_model_instance_update_no_refresh(self):
        self.site = Site.objects.get(is_default_site=True)
        self.spanish_parent_page = get_or_create_page(
            apps,
            "ask_cfpb",
            "AnswerLandingPage",
            "Obtener respuestas",
            SPANISH_PARENT_SLUG,
            self.site.root_page,
            language="es",
            live=True,
        )
        self.answer = Answer(id=1234)
        self.answer.save()
        self.page = AnswerPage(
            language="es",
            slug="mock-spanish-question-es-1234",
            title="Mock Spanish question",
            answer_base=self.answer,
            answer_content="Mock Spanish answer",
            question="Mock Spanish question",
            search_tags="Spanish",
        )
        self.spanish_parent_page.add_child(instance=self.page)
        self.page.save_revision().publish()
        doc = AnswerPageDocument()
        doc.django.auto_refresh = False
        with patch('django_elasticsearch_dsl.documents.bulk') as mock:
            doc.update(self.page)
            self.assertNotIn('refresh', mock.call_args_list[0][1])
