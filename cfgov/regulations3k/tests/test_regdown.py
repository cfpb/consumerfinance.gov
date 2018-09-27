# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import markdown

from regulations3k.regdown import (
    DEFAULT_RENDER_BLOCK_REFERENCE, extract_labeled_paragraph, regdown
)


class RegulationsExtensionTestCase(unittest.TestCase):

    def test_label(self):
        text = '{my-label} This is a paragraph with a label.'
        self.assertEqual(
            regdown(text),
            '<p class="regdown-block level-1" id="my-label">'
            'This is a paragraph with a label.</p>'
        )

    def test_nolabel(self):
        text = 'This is a paragraph without a label.'
        self.assertEqual(
            regdown(text),
            '<p class="regdown-block" '
            'id="e2cb7f25f263e65fc6737e03e0ecb90382398da3966b6da734b451be">'
            'This is a paragraph without a label.</p>'
        )

    def test_linebreak_label(self):
        text = '{my-label}\nThis is a paragraph with a label.'
        self.assertEqual(
            regdown(text),
            '<p class="regdown-block level-1" id="my-label">'
            'This is a paragraph with a label.</p>'
        )

    def test_multiple_linebreaks_label(self):
        text = '{my-label}\n\nThis is a paragraph with a label.'
        self.assertEqual(
            regdown(text),
            '<div class="regdown-block level-1" id="my-label"></div>\n'
            '<p class="regdown-block" '
            'id="725445113243d57f132b6408fa8583122d2641e591a9001f04fcde08">'
            'This is a paragraph with a label.</p>'
        )

    def test_inline_interp_label(self):
        text = '{1-a-Interp-1}\nThis is a paragraph with a label.'
        self.assertEqual(
            regdown(text),
            '<p class="regdown-block level-0" id="1-a-Interp-1">'
            'This is a paragraph with a label.</p>'
        )

    def test_deeper_inline_interp_label(self):
        text = '{1-a-Interp-1-i}\nThis is a paragraph with a label.'
        self.assertEqual(
            regdown(text),
            '<p class="regdown-block level-1" id="1-a-Interp-1-i">'
            'This is a paragraph with a label.</p>'
        )

    def test_even_deeper_inline_interp_label(self):
        text = '{1-a-Interp-1-i-a}\nThis is a paragraph with a label.'
        self.assertEqual(
            regdown(text),
            '<p class="regdown-block level-2" id="1-a-Interp-1-i-a">'
            'This is a paragraph with a label.</p>'
        )

    def test_complicated_inline_interp_label(self):
        text = '{12-d-Interp-7-ii-c-A-7}\nThis is a paragraph with a label.'
        self.assertEqual(
            regdown(text),
            '<p class="regdown-block level-4" id="12-d-Interp-7-ii-c-A-7">'
            'This is a paragraph with a label.</p>'
        )

    def test_prefixed_inline_interp_label(self):
        text = '{31-a-1-Interp-1}\nThis is a paragraph with a label.'
        text2 = '{31-a-1-i-Interp-1}\nThis is a paragraph with a label.'
        self.assertEqual(
            regdown(text),
            '<p class="regdown-block level-0" id="31-a-1-Interp-1">'
            'This is a paragraph with a label.</p>'
        )
        self.assertEqual(
            regdown(text2),
            '<p class="regdown-block level-0" id="31-a-1-i-Interp-1">'
            'This is a paragraph with a label.</p>'
        )

    def test_empty_inline_interp_label(self):
        text = (
            '{30-Interp-1}\n'
            '1. Applicability\n\n'
            '{30-b-Interp}\n'
            '#### 30(b) Business Day'
        )
        self.assertIn(
            '<div class="regdown-block level-2" id="30-b-Interp"></div>',
            regdown(text)
        )

    def test_appendix_label(self):
        text = '{A-2-d}\nThis is a paragraph with a label.'
        text2 = '{A-2-d-1}\nThis is another paragraph with a label.'
        text3 = '{A-2-d-1-v}\nThis is yet another paragraph with a label.'
        self.assertEqual(
            regdown(text),
            '<p class="regdown-block level-0" id="A-2-d">'
            'This is a paragraph with a label.</p>'
        )
        self.assertEqual(
            regdown(text2),
            '<p class="regdown-block level-1" id="A-2-d-1">'
            'This is another paragraph with a label.</p>'
        )
        self.assertEqual(
            regdown(text3),
            '<p class="regdown-block level-2" id="A-2-d-1-v">'
            'This is yet another paragraph with a label.</p>'
        )

    def test_multi_part_appendix_label(self):
        text = '{M1-1-a}\nThis is a paragraph with a label.'
        text2 = '{M1-1-a-1}\nThis is another paragraph with a label.'
        text3 = '{M1-1-a-1-i}\nThis is yet another paragraph with a label.'
        self.assertEqual(
            regdown(text),
            '<p class="regdown-block level-0" id="M1-1-a">'
            'This is a paragraph with a label.</p>'
        )
        self.assertEqual(
            regdown(text2),
            '<p class="regdown-block level-1" id="M1-1-a-1">'
            'This is another paragraph with a label.</p>'
        )
        self.assertEqual(
            regdown(text3),
            '<p class="regdown-block level-2" id="M1-1-a-1-i">'
            'This is yet another paragraph with a label.</p>'
        )

    def test_complex_appendix_label(self):
        text = '{B-h2-p2}\nThis is a paragraph with a label.'
        text2 = '{B-h2-p2-1}\nThis is another paragraph with a label.'
        text3 = '{B-h2-p2-1-i}\nThis is yet another paragraph with a label.'
        self.assertEqual(
            regdown(text),
            '<p class="regdown-block level-0" id="B-h2-p2">'
            'This is a paragraph with a label.</p>'
        )
        self.assertEqual(
            regdown(text2),
            '<p class="regdown-block level-1" id="B-h2-p2-1">'
            'This is another paragraph with a label.</p>'
        )
        self.assertEqual(
            regdown(text3),
            '<p class="regdown-block level-2" id="B-h2-p2-1-i">'
            'This is yet another paragraph with a label.</p>'
        )

    def test_list_state(self):
        text = '- {my-label} This is a paragraph in a list.'
        self.assertEqual(
            regdown(text),
            '<ul>\n<li>\n<p class="regdown-block level-1" id="my-label">'
            'This is a paragraph in a list.'
            '</p>\n</li>\n</ul>'
        )

    def test_makeExtension(self):
        """ Test that Markdown can load our extension from a string """
        try:
            markdown.Markdown(extensions=['regulations3k.regdown'])
        except AttributeError as e:  # pragma: no cover
            self.fail('Markdown failed to load regdown extension: '
                      '{}'.format(e.message))

    def test_block_reference_resolver_not_callable(self):
        text = 'see(foo-bar)'
        self.assertEqual(
            regdown(
                text,
                contents_resolver=None,
                render_block_reference=DEFAULT_RENDER_BLOCK_REFERENCE
            ),
            ''
        )

    def test_block_reference_renderer_not_callable(self):
        text = 'see(foo-bar)'
        self.assertEqual(regdown(text, render_block_reference=None), '')

    def test_block_reference_no_contents(self):
        contents_resolver = lambda l: ''
        text = 'see(foo-bar)'
        self.assertEqual(
            regdown(
                text,
                contents_resolver=contents_resolver,
                render_block_reference=DEFAULT_RENDER_BLOCK_REFERENCE
            ),
            ''
        )

    def test_block_reference(self):
        contents_resolver = lambda l: '{foo-bar}\n# §FooBar\n\n'
        text = 'see(foo-bar)'
        self.assertIn(
            '<h1>§FooBar</h1>',
            regdown(
                text,
                contents_resolver=contents_resolver,
                render_block_reference=DEFAULT_RENDER_BLOCK_REFERENCE
            )
        )

    def test_tables_extension_exists(self):
        text = (
            'First Header  | Second Header\n'
            '------------- | -------------\n'
            'Content Cell  | Content Cell\n'
            'Content Cell  | Content Cell\n'
        )
        self.assertIn('<table>', regdown(text))
        self.assertIn('<th>First Header</th>', regdown(text))
        self.assertIn('<td>Content Cell</td>', regdown(text))

    def test_no_underscore_emphasis(self):
        self.assertIn('<em>foo</em>', regdown('*foo*'))
        self.assertIn('<strong>foo</strong>', regdown('**foo**'))
        self.assertIn('<strong><em>foo</em></strong>', regdown('***foo***'))
        self.assertNotIn('<em>foo</em>', regdown('_foo_'))
        self.assertNotIn('<strong>foo</strong>', regdown('__foo__'))
        self.assertNotIn('<strong><em>foo</em></strong>', regdown('___foo___'))

    def test_pseudo_form_field_end_of_line(self):
        text = 'Form field: ___'
        self.assertIn('Form field: '
                      '<span class="regdown-form_extend">___'
                      '<span></span></span>',
                      regdown(text))

    def test_pseudo_form_field_start_of_line(self):
        text = '__Form Field'
        self.assertIn('<span class="regdown-form">__</span>Form Field',
                      regdown(text))

    def test_pseudo_form_field_inside_line(self):
        text = 'inline______fields______within paragraph'
        self.assertIn(
            'inline<span class="regdown-form">______</span>'
            'fields<span class="regdown-form">______</span>'
            'within paragraph',
            regdown(text)
        )

    def test_pseudo_form_field_number_of_underscores(self):
        self.assertIn('<span class="regdown-form_extend">__'
                      '<span></span></span>',
                      regdown('Field: __'))
        self.assertIn('<span class="regdown-form_extend">_______'
                      '<span></span></span>',
                      regdown('Field: _______'))

    def test_section_symbol_with_non_breaking_space(self):
        self.assertIn('§&#160;1023', regdown('§ 1023'))
        self.assertIn('§&#160;1023.4', regdown('§ 1023.4'))
        self.assertIn('§&#160;1023.4(a)', regdown('§ 1023.4(a)'))
        self.assertIn('§&#160;1023.4(a)', regdown('§\t1023.4(a)'))
        self.assertIn('§&#160;1023.4(a)', regdown('§      1023.4(a)'))
        self.assertIn('§&#160;1023.4(a)', regdown('§&#160;1023.4(a)'))


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
