# Based on https://github.com/django-es/django-elasticsearch-dsl/blob/master/tests/test_documents.py  # noqa
from unittest import TestCase

from django.db import models

from django_elasticsearch_dsl import fields
from django_elasticsearch_dsl.documemts import DocType
from django_elasticsearch_dsl.exceptions import ModelFieldNotMappedError
from mock import patch

from ask_cfpb.documents import AnswerPageDocument
from ask_cfpb.models import Answer, AnswerPage


class AnswerPageDocumentCase(TestCase):

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
                    'autocomplete', 'portal_categories', 'text',
                    'url', 'preview', 'search_tags', 'language'
                ]
            )
        )

    def test_related_models_added(self):
        related_models = AnswerPageDocument.django.related_models
        self.assertEqual([Answer], related_models)

    def test_to_field(self):
        doc = DocType()
        answer_page_text_fields = [
            'autocomplete',
            'portal_categories',
            'text',
            'url',
            'preview',
            'search_tags',
            'language'
        ]
        for f in answer_page_text_fields:
            nameField = doc.to_field(f, AnswerPage._meta.get_field(f))
            self.assertIsInstance(nameField, fields.TextField)
            self.assertEqual(nameField._path, [f])
        topicField = doc.to_field(
            'portal_topics', AnswerPage._meta.get_field('portal_topics')
        )
        self.assertIsInstance(topicField, fields.KeywordField)
        self.assertEqual(topicField._path, ['portal_topics'])

    def test_to_field_with_unknown_field(self):
        doc = DocType()
        with self.assertRaises(ModelFieldNotMappedError):
            doc.to_field('document', AnswerPage._meta.get_field('document'))

    def test_mapping(self):
        self.assertEqual(
            AnswerPageDocument._doc_type.mapping.to_dict(), {
                'properties': {
                    'autocomplete': {
                        'type': 'text'
                    },
                    'portal_categories': {
                        'type': 'text'
                    },
                    'url': {
                        'type': 'text'
                    },
                    'preview': {
                        'type': 'text'
                    },
                    'search_tags': {
                        'type': 'text'
                    },
                    'language': {
                        'type': 'text'
                    }
                }
            }
        )

    def test_get_queryset(self):
        qs = AnswerPageDocument().get_queryset()
        self.assertIsInstance(qs, models.QuerySet)
        self.assertEqual(qs.model, AnswerPage)

    def test_prepare(self):
        answer_page = AnswerPage()
        doc = AnswerPageDocument()
        prepared_data = doc.prepare(answer_page)
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
        doc = AnswerPageDocument()
        doc.django.auto_refresh = False
        answer_page = AnswerPage()
        with patch('django_elasticsearch_dsl.documents.bulk') as mock:
            doc.update(answer_page)
            self.assertNotIn('refresh', mock.call_args_list[0][1])
