from __future__ import unicode_literals

from django.test import TestCase, override_settings

from ask_cfpb.models.blocks import AskAnswerContent, Tip


@override_settings(LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),))
class AskBlocksTestCase(TestCase):
    def setUp(self):
        self.tip_content = {
            'content': 'Tip content'
        }
        self.tip_data = {
            'type': 'tip',
            'value': self.tip_content
        }
        self.expected_tip_html = (
            '<aside class="m-inset m-inset__bordered">'
            '<h4>Tip</h4>'
            '<div class="rich-text">Tip content</div>'
            '</aside>'
        )
        self.text_data = {
            'type': 'text',
            'value': {
                'content': 'text'
            }
        }
        self.expected_text_html = '<div class="rich-text">text</div>'

    def test_tip_block_renders_html(self):
        block = Tip()
        html = block.render(self.tip_content)
        self.assertHTMLEqual(html, self.expected_tip_html)

    def test_content_block_applies_wrapper_to_tip(self):
        block = AskAnswerContent()
        value = block.to_python([self.tip_data])
        html = block.render(value)
        expected_html = '<div class="inset-row">{}</div>'.format(
            self.expected_tip_html
        )
        self.assertHTMLEqual(html, expected_html)

    def test_content_block_applies_wrapper_to_tip_and_next_block(self):
        block = AskAnswerContent()
        value = block.to_python([self.tip_data, self.text_data])
        html = block.render(value)
        expected_html = '<div class="inset-row">{}{}</div>'.format(
            self.expected_tip_html,
            self.expected_text_html
        )
        self.assertHTMLEqual(html, expected_html)

    def test_content_block_does_not_apply_wrapper_without_tip(self):
        block = AskAnswerContent()
        value = block.to_python([self.text_data])
        html = block.render(value)
        self.assertNotIn('<div class="inset-row">', html)
        self.assertHTMLEqual(html, self.expected_text_html)
