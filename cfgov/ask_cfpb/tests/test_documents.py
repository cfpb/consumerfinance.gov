# Based on https://github.com/django-es/django-elasticsearch-dsl/blob/master/tests/test_documents.py  # noqa
from unittest import TestCase

from django.db import models

from wagtail.core.blocks import StreamValue

from django_elasticsearch_dsl import fields
from django_elasticsearch_dsl.documents import DocType
from django_elasticsearch_dsl.exceptions import ModelFieldNotMappedError
from mock import patch

from ask_cfpb.documents import AnswerPageDocument
from ask_cfpb.models import Answer, AnswerPage


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
                    'text': {'analyzer': 'synonym_analyzer_en', 'type': 'text'},
                    'url': {'type': 'text'}
                }
            }
        )

    def test_get_queryset(self):
        qs = AnswerPageDocument().get_queryset()
        self.assertIsInstance(qs, models.QuerySet)
        self.assertEqual(qs.model, AnswerPage)

    def test_prepare(self):
        answer = Answer(id=1234)
        answer.save()
        page = AnswerPage(
            slug="mock-question-en-1234", title="Mock question"
        )
        page.answer_base = answer
        page.question = "Mock question"
        page.answer_content = StreamValue(
            page.answer_content.stream_block,
            [{"type": "text", "value": {"content": "Mock answer"}}],
            True,
        )
        doc = AnswerPageDocument()
        prepared_data = doc.prepare(page)
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
        answer = Answer(id=1234)
        answer.save()
        page = AnswerPage(
            slug="mock-question-en-1234", title="Mock question"
        )
        page.answer_base = answer
        page.question = "Mock question"
        page.answer_content = StreamValue(
            page.answer_content.stream_block,
            [{"type": "text", "value": {"content": "Mock answer"}}],
            True,
        )
        doc = AnswerPageDocument()
        doc.django.auto_refresh = False
        with patch('django_elasticsearch_dsl.documents.bulk') as mock:
            doc.update(page)
            self.assertNotIn('refresh', mock.call_args_list[0][1])
