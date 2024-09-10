from django.test import TestCase, override_settings

from ask_cfpb.models.blocks import AskAnswerContent, Tip
from v1.atomic_elements.schema import FAQ, HowTo


@override_settings(LANGUAGE_CODE="en-US", LANGUAGES=(("en", "English"),))
class AskBlocksTestCase(TestCase):
    def setUp(self):
        self.tip_content = {"content": "Tip content"}
        self.tip_data = {"type": "tip", "value": self.tip_content}
        self.expected_tip_html = (
            '<aside class="m-inset m-inset--bordered">'
            "<h4>Tip</h4>"
            "Tip content"
            "</aside>"
        )
        self.expected_text_html = "text"
        self.text_data = {"type": "text", "value": {"content": "text"}}

    def test_tip_block_renders_html(self):
        block = Tip()
        html = block.render(self.tip_content)
        self.assertHTMLEqual(html, self.expected_tip_html)

    def test_content_block_applies_wrapper_to_tip(self):
        block = AskAnswerContent()
        value = block.to_python([self.tip_data])
        html = block.render(value)
        expected_html = f'<div class="row">{self.expected_tip_html}</div>'
        self.assertHTMLEqual(html, expected_html)

    def test_content_block_applies_wrapper_to_tip_and_next_block(self):
        block = AskAnswerContent()
        value = block.to_python([self.tip_data, self.text_data])
        html = block.render(value)
        expected_html = f'<div class="row">{self.expected_tip_html}{self.expected_text_html}</div>'  # noqa: E501
        self.assertHTMLEqual(html, expected_html)

    def test_content_block_does_not_apply_wrapper_without_tip(self):
        block = AskAnswerContent()
        value = block.to_python([self.text_data])
        html = block.render(value)
        expected_html = f'<div class="row">{self.expected_text_html}</div>'
        self.assertNotIn('<div class="row">', html)
        self.assertHTMLEqual(html, expected_html)


class SchemaBlocksTestCase(TestCase):
    def test_how_to_block_renders_schema(self):
        block = HowTo()
        data = {
            "title": "test title",
            "show_title": True,
            "title_tag": "h2",
            "description": "test description",
            "step_title_tag": "p",
            "has_numbers": True,
            "steps": [{"title": "Step one", "step_content": "Step content"}],
        }
        expected_html = (
            "<div itemscope"
            '     itemtype="https://schema.org/HowTo"'
            '     class="schema-block schema-block--how-to">'
            '<h2 itemprop="name" class="schema-block_title" id="test-title">'
            "test title</h2>"  # noqa
            '<div itemprop="description" class="schema-block_description">'
            "test description"
            "</div>"
            "<ol>"
            '<li class="schema-block_item">'
            '<div itemprop="step"'
            "     itemscope"
            '     itemtype="https://schema.org/HowToStep">'
            '<p itemprop="name">Step one</p>'
            '<div itemprop="text">Step content</div>'
            "</div>"
            "</li>"
            "</ol>"
            "</div>"
        )
        html = block.render(data)
        self.assertHTMLEqual(html, expected_html)

    def test_faq_block_renders_schema(self):
        block = FAQ()
        data = {
            "description": "test description",
            "questions": [
                {
                    "question": "Question one",
                    "answer_content": "Answer content",
                }
            ],
        }
        expected_html = (
            '<div itemscope itemtype="https://schema.org/FAQPage" '
            'class="schema-block schema-block--faq">'
            '<div itemprop="description" class="schema-block_description">'
            "test description"
            "</div>"
            '<div itemscope itemprop="mainEntity" '
            'itemtype="https://schema.org/Question" class="schema-block_item">'  # noqa
            '<h2 itemprop="name">Question one</h2>'
            '<div itemprop="acceptedAnswer" itemscope '
            'itemtype="https://schema.org/Answer">'
            '<div itemprop="text">Answer content</div>'
            "</div>"
            "</div>"
            "</div>"
        )
        html = block.render(data)
        self.assertHTMLEqual(html, expected_html)
