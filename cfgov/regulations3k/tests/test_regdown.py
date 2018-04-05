import unittest

import markdown
from regulations3k.regdown import regdown


class RegulationsExtensionTestCase(unittest.TestCase):

    def test_label(self):
        text = '{my-label} This is a paragraph with a label.'
        self.assertEqual(
            regdown(text),
            '<p id="my-label">This is a paragraph with a label.</p>'
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
            '<p id="my-label">This is a paragraph with a label.</p>'
        )

    def test_multiple_linebreaks_label(self):
        text = '{my-label}\n\nThis is a paragraph with a label.'
        self.assertEqual(
            regdown(text),
            '<p id="my-label"></p>\n'
            '<p id="725445113243d57f132b6408fa8583122d2641e591a9001f04fcde08">'
            'This is a paragraph with a label.</p>'
        )

    def test_list_state(self):
        text = '- {my-label} This is a paragraph in a list.'
        self.assertEqual(
            regdown(text),
            '<ul>\n<li>\n<p id="my-label">This is a paragraph in a list.'
            '</p>\n</li>\n</ul>'
        )

    def test_makeExtension(self):
        """ Test that Markdown can load our extension from a string """
        try:
            markdown.Markdown(extensions=['regulations3k.regdown'])
        except AttributeError as e:
            self.fail('Markdown failed to load regdown extension: '
                      '{}'.format(e.message))
