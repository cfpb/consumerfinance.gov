# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import markdown
from regulations3k.regdown import extract_labeled_paragraph, regdown


class RegulationsExtensionTestCase(unittest.TestCase):

    def test_label(self):
        text = '{my-label} This is a paragraph with a label.'
        self.assertEqual(
            regdown(text),
            '<p class="level-1" id="my-label">'
            'This is a paragraph with a label.</p>'
        )

    def test_nolabel(self):
        text = 'This is a paragraph without a label.'
        self.assertEqual(
            regdown(text),
            '<p id="e2cb7f25f263e65fc6737e03e0ecb90382398da3966b6da734b451be">'
            'This is a paragraph without a label.</p>'
        )

    def test_linebreak_label(self):
        text = '{my-label}\nThis is a paragraph with a label.'
        self.assertEqual(
            regdown(text),
            '<p class="level-1" id="my-label">'
            'This is a paragraph with a label.</p>'
        )

    def test_multiple_linebreaks_label(self):
        text = '{my-label}\n\nThis is a paragraph with a label.'
        self.assertEqual(
            regdown(text),
            '<p class="level-1" id="my-label"></p>\n'
            '<p id="725445113243d57f132b6408fa8583122d2641e591a9001f04fcde08">'
            'This is a paragraph with a label.</p>'
        )

    def test_inline_interp_label(self):
        text = '{1-a-Interp-1}\nThis is a paragraph with a label.'
        self.assertEqual(
            regdown(text),
            '<p class="level-1" id="1-a-Interp-1">'
            'This is a paragraph with a label.</p>'
        )

    def test_deeper_inline_interp_label(self):
        text = '{1-a-Interp-1-i}\nThis is a paragraph with a label.'
        self.assertEqual(
            regdown(text),
            '<p class="level-2" id="1-a-Interp-1-i">'
            'This is a paragraph with a label.</p>'
        )

    def test_even_deeper_inline_interp_label(self):
        text = '{1-a-Interp-1-i-a}\nThis is a paragraph with a label.'
        self.assertEqual(
            regdown(text),
            '<p class="level-3" id="1-a-Interp-1-i-a">'
            'This is a paragraph with a label.</p>'
        )

    def test_complicated_inline_interp_label(self):
        text = '{12-d-Interp-7-ii-c-A-7}\nThis is a paragraph with a label.'
        self.assertEqual(
            regdown(text),
            '<p class="level-5" id="12-d-Interp-7-ii-c-A-7">'
            'This is a paragraph with a label.</p>'
        )

    def test_list_state(self):
        text = '- {my-label} This is a paragraph in a list.'
        self.assertEqual(
            regdown(text),
            '<ul>\n<li>\n<p class="level-1" id="my-label">'
            'This is a paragraph in a list.'
            '</p>\n</li>\n</ul>'
        )

    def test_makeExtension(self):
        """ Test that Markdown can load our extension from a string """
        try:
            markdown.Markdown(extensions=['regulations3k.regdown'])
        except AttributeError as e:
            self.fail('Markdown failed to load regdown extension: '
                      '{}'.format(e.message))

    def test_block_reference_resolver_not_callable(self):
        text = 'see(foo-bar)'
        self.assertEqual(regdown(text, contents_resolver=None), '')

    def test_block_reference_renderer_not_callable(self):
        text = 'see(foo-bar)'
        self.assertEqual(regdown(text, render_block_reference=None), '')

    def test_block_reference_no_contents(self):
        contents_resolver = lambda l: ''
        text = 'see(foo-bar)'
        self.assertEqual(
            regdown(text, contents_resolver=contents_resolver),
            ''
        )

    def test_block_reference(self):
        contents_resolver = lambda l: '{foo-bar}\n# §FooBar\n\n'
        text = 'see(foo-bar)'
        self.assertIn('<h1>§FooBar</h1>',
                      regdown(text, contents_resolver=contents_resolver))


class RegdownUtilsTestCase(unittest.TestCase):

    def test_extract_labeled_paragraph(self):
        text = (
            '{first-label} First para\n\n'
            '{my-label} Second para\n\n'
            'Third para\n\n'
            '{next-label}Fourth para'
        )
        result = extract_labeled_paragraph('my-label', text)
        self.assertIn('Second para', result)
        self.assertIn('Third para', result)

    def test_extract_labeled_paragraph_not_found(self):
        text = (
            '{another-label} First para\n\n'
            '{next-label}Fourth para'
        )
        result = extract_labeled_paragraph('my-label', text)
        self.assertEqual(result, '')

    def test_extract_labeled_paragraph_startswith(self):
        text = (
            '{first-label} First para\n\n'
            '{my-label} Second para\n\n'
            'Third para\n\n'
            '{my-label-1}Fourth para\n\n'
            '{my-label-2}Fifth para\n\n'
            '{next-label}Sixth para\n\n'
        )
        result = extract_labeled_paragraph('my-label', text, exact=False)
        self.assertIn('Second para', result)
        self.assertIn('Third para', result)
        self.assertIn('Fourth para', result)
        self.assertIn('Fifth para', result)
