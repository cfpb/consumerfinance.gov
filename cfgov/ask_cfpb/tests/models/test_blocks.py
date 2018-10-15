# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

from django.core.exceptions import ObjectDoesNotExist, ValidationError

from mock import patch
from model_mommy import mommy

from ask_cfpb.models.blocks import (
    AskItem, AskLinkItem, AskTextItem, LinkItem, TextItem
)
from ask_cfpb.models.django import Answer


class AskItemTest(unittest.TestCase):
    @patch('ask_cfpb.models.django.Answer.objects')
    def test_success(self, mock_answer):
        mock_answer.get.return_value = True
        block = AskItem()
        value = block.to_python({'answer_id': 1234})
        try:
            block.clean(value)
        except ValidationError:
            self.fail(
                'An AskLinkItem with a valid answer id should not error.'
            )

    @patch('ask_cfpb.models.django.Answer.objects')
    def test_failure(self, mock_answer):
        mock_answer.get.side_effect = ObjectDoesNotExist
        block = AskItem()
        value = block.to_python({'answer_id': 1234})
        with self.assertRaises(ValidationError):
            block.clean(value)


class AskLinkItemTest(unittest.TestCase):
    def setUp(self):
        self.answer = mommy.prepare(
            Answer,
            id=1234,
            answer='Test answer',
            statement='Test statement',
            slug='test-answer-en-1234',
            question='Test question'
        )

    @patch('ask_cfpb.models.django.Answer.objects')
    def test_context_with_answer(self, mock_answer):
        mock_answer.get.return_value = self.answer
        block = AskLinkItem()
        value = block.to_python({
            'answer_id': 1234
        })
        ctx = block.get_context(value)
        self.assertEqual(
            ctx['answer'],
            self.answer
        )
        self.assertEqual(
            ctx['link_text'],
            self.answer.statement
        )

    @patch('ask_cfpb.models.django.Answer.objects')
    def test_context_with_answer_and_overridden_text(self, mock_answer):
        mock_answer.get.return_value = self.answer
        block = AskLinkItem()
        link_text = 'Alternate text'
        value = block.to_python({
            'answer_id': 1234,
            'link_text': link_text
        })
        ctx = block.get_context(value)
        self.assertEqual(
            ctx['answer'],
            self.answer
        )
        self.assertEqual(
            ctx['link_text'],
            link_text
        )

    @patch('ask_cfpb.models.django.Answer.objects')
    def test_context_without_answer(self, mock_answer):
        mock_answer.get.return_value = None
        block = AskLinkItem()
        value = block.to_python({'answer_id': 1234})
        self.assertEqual(block.get_context(value), None)


class AskTextItemTest(unittest.TestCase):
    def setUp(self):
        self.answer = mommy.prepare(
            Answer,
            id=1234,
            answer='Test answer',
            statement='Test statement',
            slug='test-answer-en-1234',
            question='Test question'
        )

    @patch('ask_cfpb.models.django.Answer.objects')
    def test_context_with_answer(self, mock_answer):
        mock_answer.get.return_value = self.answer
        block = AskTextItem()
        block_obj = {
            'answer_id': 1234,
            'heading_level': 'h3',
            'body': 'Test body text',
            'link_text': 'Test link text'
        }
        value = block.to_python(block_obj)
        ctx = block.get_context(value)
        self.assertEqual(ctx['answer'], self.answer)
        self.assertEqual(ctx['heading'], self.answer.statement)
        self.assertEqual(ctx['heading_level'], block_obj['heading_level'])
        self.assertEqual(ctx['body'], block_obj['body'])
        self.assertEqual(ctx['link_text'], block_obj['link_text'])

    @patch('ask_cfpb.models.django.Answer.objects')
    def test_context_with_answer_and_overridden_heading(self, mock_answer):
        mock_answer.get.return_value = self.answer
        block = AskTextItem()
        block_obj = {
            'answer_id': 1234,
            'heading': 'Test heading',
            'heading_level': 'h3',
            'body': 'Test body text',
            'link_text': 'Text link text'
        }
        value = block.to_python(block_obj)
        ctx = block.get_context(value)
        self.assertEqual(ctx['answer'], self.answer)
        self.assertEqual(ctx['heading'], block_obj['heading'])
        self.assertEqual(ctx['heading_level'], block_obj['heading_level'])
        self.assertEqual(ctx['body'], block_obj['body'])
        self.assertEqual(ctx['link_text'], block_obj['link_text'])

    @patch('ask_cfpb.models.django.Answer.objects')
    def test_context_without_answer(self, mock_answer):
        mock_answer.get.return_value = None
        block = AskTextItem()
        value = block.to_python({'answer_id': 1234})
        self.assertEqual(block.get_context(value), None)


class LinkItemTest(unittest.TestCase):
    def test_context(self):
        block = LinkItem()
        block_obj = {
            'link_text': 'Link text',
            'external_link': '/link'
        }
        value = block.to_python(block_obj)
        ctx = block.get_context(value)
        self.assertEqual(ctx['link_text'], block_obj['link_text'])
        self.assertEqual(ctx['external_link'], block_obj['external_link'])


class TextItemTest(unittest.TestCase):
    def test_context(self):
        block = TextItem()
        block_obj = {
            'heading': 'Test heading',
            'heading_level': 'h3',
            'body': 'Test body text',
            'link_text': 'Text link text'
        }
        value = block.to_python(block_obj)
        ctx = block.get_context(value)
        self.assertEqual(ctx['heading'], block_obj['heading'])
        self.assertEqual(ctx['heading_level'], block_obj['heading_level'])
        self.assertEqual(ctx['body'], block_obj['body'])
        self.assertEqual(ctx['link_text'], block_obj['link_text'])
