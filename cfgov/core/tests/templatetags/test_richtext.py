from unittest import TestCase

from core.templatetags.richtext import richtext_isempty


class TestRichTextIsEmpty(TestCase):
    def test_none(self):
        self.assertTrue(richtext_isempty(None))

    def test_empty_string(self):
        self.assertTrue(richtext_isempty(''))

    def test_empty_paragraphs(self):
        self.assertTrue(richtext_isempty('<p></p>'))

    def test_not_empty(self):
        self.assertFalse(richtext_isempty('<p>Paragraph with content</p>'))
