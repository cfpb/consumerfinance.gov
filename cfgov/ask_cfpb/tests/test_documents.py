# Based on https://github.com/django-es/django-elasticsearch-dsl/blob/master/tests/test_documents.py  # noqa
import json
from unittest.mock import patch

from django.db import models
from django.test import TestCase, override_settings

from wagtail.models import Site

from django_opensearch_dsl import fields
from django_opensearch_dsl.documents import Document
from django_opensearch_dsl.exceptions import ModelFieldNotMappedError
from model_bakery import baker

from ask_cfpb.documents import AnswerPageDocument
from ask_cfpb.models.answer_page import AnswerPage
from ask_cfpb.models.django import (
    ENGLISH_PARENT_SLUG,
    SPANISH_PARENT_SLUG,
    Answer,
)
from ask_cfpb.models.pages import AnswerLandingPage
from v1.models import PortalCategory, PortalTopic, SublandingPage


class AnswerPageDocumentTest(TestCase):
    def setUp(self):
        self.site = Site.objects.get(is_default_site=True)
        self.root_page = self.site.root_page
        self.portal_topic = baker.make(
            PortalTopic, heading="test topic", heading_es="prueba tema"
        )
        self.en_portal_category = baker.make(
            PortalCategory, heading="test_english_heading"
        )
        self.es_portal_category = baker.make(
            PortalCategory, heading="test_spanish_heading"
        )
        self.en_portal_page = SublandingPage(
            title="test English portal page",
            slug="test-en-portal-page",
            portal_topic=self.portal_topic,
            language="en",
        )
        self.es_portal_page = SublandingPage(
            title="test Spanish portal page",
            slug="test-es-portal-page",
            portal_topic=self.portal_topic,
            language="es",
        )
        self.root_page.add_child(instance=self.en_portal_page)
        self.en_portal_page.save()
        self.en_portal_page.save_revision().publish()

        self.en_parent_page = AnswerLandingPage(
            title="Ask CFPB",
            slug=ENGLISH_PARENT_SLUG,
            language="en",
            live=True,
        )
        self.root_page.add_child(instance=self.en_parent_page)

        self.es_parent_page = AnswerLandingPage(
            title="Obtener respuestas",
            slug=SPANISH_PARENT_SLUG,
            language="es",
            live=True,
        )
        self.root_page.add_child(instance=self.es_parent_page)

        self.answer = Answer(id=1234)
        self.answer.save()
        self.en_page = AnswerPage(
            language="en",
            slug="test-english-question-en-1234",
            title="Test English question",
            answer_base=self.answer,
            answer_content=json.dumps(
                [
                    {
                        "type": "text",
                        "value": {
                            "anchor_tag": "",
                            "content": "Test English answer",
                        },
                    }
                ]
            ),
            question="Test English question",
            search_tags="English",
        )
        self.es_page = AnswerPage(
            language="es",
            slug="test-spanish-question-es-1234",
            title="Test Spanish question",
            answer_base=self.answer,
            answer_content=json.dumps(
                [
                    {
                        "type": "text",
                        "value": {
                            "anchor_tag": "",
                            "content": "Test Spanish answer",
                        },
                    }
                ]
            ),
            question="Test Spanish question",
            search_tags="Spanish",
        )
        self.doc = AnswerPageDocument()

    def test_model_class_added(self):
        self.assertEqual(AnswerPageDocument.django.model, AnswerPage)

    def test_ignore_signal_default(self):
        self.assertFalse(AnswerPageDocument.django.ignore_signals)

    def test_auto_refresh_default(self):
        self.assertFalse(AnswerPageDocument.Index.auto_refresh)

    def test_fields_populated(self):
        mapping = AnswerPageDocument._doc_type.mapping
        self.assertEqual(
            set(mapping.properties.properties.to_dict().keys()),
            set(
                [
                    "answer_id",
                    "autocomplete",
                    "portal_categories",
                    "portal_topics",
                    "text",
                    "url",
                    "preview",
                    "search_tags",
                    "language",
                ]
            ),
        )

    def test_to_field(self):
        doc = Document()
        for f in ["question"]:
            nameField = doc.to_field(f, AnswerPage._meta.get_field(f))
            self.assertIsInstance(nameField, fields.TextField)
            self.assertEqual(nameField._path, [f])
        dateField = doc.to_field(
            "last_edited", AnswerPage._meta.get_field("last_edited")
        )
        self.assertIsInstance(dateField, fields.DateField)
        self.assertEqual(dateField._path, ["last_edited"])

    def test_to_field_with_unknown_field(self):
        doc = Document()
        with self.assertRaises(ModelFieldNotMappedError):
            doc.to_field(
                "answer_base", AnswerPage._meta.get_field("answer_base")
            )

    def test_mapping(self):
        self.assertEqual(
            AnswerPageDocument._doc_type.mapping.to_dict(),
            {
                "properties": {
                    "autocomplete": {
                        "analyzer": "ngram_tokenizer",
                        "type": "text",
                        "fields": {"raw": {"type": "keyword"}},
                    },
                    "language": {"type": "text"},
                    "portal_categories": {"type": "text"},
                    "portal_topics": {"type": "keyword"},
                    "preview": {"type": "text"},
                    "search_tags": {"type": "text"},
                    "text": {"analyzer": "synonym_analyzer", "type": "text"},
                    "url": {"type": "text"},
                    "answer_id": {"type": "keyword"},
                }
            },
        )

    def test_get_queryset(self):
        qs = AnswerPageDocument().get_queryset()
        self.assertIsInstance(qs, models.QuerySet)
        self.assertEqual(qs.model, AnswerPage)

    def test_prepare_en(self):
        self.en_parent_page.add_child(instance=self.en_page)
        self.en_page.save_revision().publish()
        en_prepared_data = self.doc.prepare(self.en_page)
        self.assertEqual(
            en_prepared_data,
            {
                "answer_id": 1234,
                "autocomplete": self.doc.prepare_autocomplete(self.en_page),
                "language": "en",
                "portal_categories": self.doc.prepare_portal_categories(
                    self.en_page
                ),
                "portal_topics": self.doc.prepare_portal_topics(self.en_page),
                "preview": "Test English answer",
                "search_tags": self.doc.prepare_search_tags(self.en_page),
                "text": "Test English question\nTest English answer",
                "url": self.doc.prepare_url(self.en_page),
            },
        )

    def test_prepare_es(self):
        self.es_parent_page.add_child(instance=self.es_page)
        self.es_page.save_revision().publish()
        es_prepared_data = self.doc.prepare(self.es_page)
        self.assertEqual(
            es_prepared_data,
            {
                "answer_id": 1234,
                "autocomplete": self.doc.prepare_autocomplete(self.es_page),
                "language": "es",
                "portal_categories": self.doc.prepare_portal_categories(
                    self.es_page
                ),
                "portal_topics": self.doc.prepare_portal_topics(self.es_page),
                "preview": "Test Spanish answer",
                "search_tags": self.doc.prepare_search_tags(self.es_page),
                "text": "Test Spanish question\nTest Spanish answer",
                "url": self.doc.prepare_url(self.es_page),
            },
        )

    @override_settings(OPENSEARCH_DSL_AUTO_REFRESH=True)
    def test_model_instance_update_no_refresh(self):
        self.es_parent_page.add_child(instance=self.es_page)
        self.es_page.save_revision().publish()
        self.doc.Index.auto_refresh = False
        with patch("django_opensearch_dsl.documents.bulk") as mock:
            self.doc.update(self.es_page, "update")
            self.assertFalse(mock.call_args_list[0][1]["refresh"])
