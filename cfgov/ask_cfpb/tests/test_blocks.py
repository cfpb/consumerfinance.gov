from django.test import TestCase, override_settings

from ask_cfpb.models.blocks import (
    FAQ,
    AskAnswerContent,
    AskContent,
    HowTo,
    Tip,
)


@override_settings(LANGUAGE_CODE="en-US", LANGUAGES=(("en", "English"),))
class AskBlocksTestCase(TestCase):
    def setUp(self):
        self.tip_content = {"content": "Tip content"}
        self.tip_data = {"type": "tip", "value": self.tip_content}
        self.expected_tip_html = (
            '<aside class="m-inset m-inset__bordered">'
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
        expected_html = '<div class="inset-row row">{}</div>'.format(
            self.expected_tip_html
        )
        self.assertHTMLEqual(html, expected_html)

    def test_content_block_applies_wrapper_to_tip_and_next_block(self):
        block = AskAnswerContent()
        value = block.to_python([self.tip_data, self.text_data])
        html = block.render(value)
        expected_html = '<div class="inset-row row">{}{}</div>'.format(
            self.expected_tip_html, self.expected_text_html
        )
        self.assertHTMLEqual(html, expected_html)

    def test_content_block_does_not_apply_wrapper_without_tip(self):
        block = AskAnswerContent()
        value = block.to_python([self.text_data])
        html = block.render(value)
        expected_html = '<div class="text-row row">{}</div>'.format(
            self.expected_text_html
        )
        self.assertNotIn('<div class="inset-row row">', html)
        self.assertHTMLEqual(html, expected_html)


class SchemaBlocksTestCase(TestCase):
    def test_how_to_block_renders_schema(self):
        block = HowTo()
        data = {
            "title": "test title",
            "description": "test description",
            "steps": [{"title": "Step one", "step_content": "Step content"}],
        }
        expected_html = (
            "<div itemscope"
            '     itemtype="http://schema.org/HowTo"'
            '     class="schema-block schema-block__how-to">'
            '<h2 itemprop="name" class="schema-block_title">test title</h2>'  # noqa
            '<div itemprop="description" class="schema-block_description">'
            "test description"
            "</div>"
            "<ol>"
            '<li itemprop="step"'
            "     itemscope"
            '     itemtype="http://schema.org/HowToStep"'
            '     class="schema-block_item">'
            '<h3 itemprop="name" class="h4">Step one</h3>'
            '<div itemprop="text">Step content</div>'
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
            '<div itemscope="" itemtype="http://schema.org/FAQPage" '
            'class="schema-block schema-block__faq">'
            '<div itemprop="description" class="schema-block_description">'
            "test description"
            "</div>"
            '<div itemscope="" itemprop="mainEntity" '
            'itemtype="http://schema.org/Question" class="schema-block_item">'  # noqa
            '<h2 itemprop="name">Question one</h2>'
            '<div itemprop="acceptedAnswer" itemscope="" '
            'itemtype="http://schema.org/Answer">'
            '<div itemprop="text">Answer content</div>'
            "</div>"
            "</div>"
            "</div>"
        )
        html = block.render(data)
        self.assertHTMLEqual(html, expected_html)


class AskContentTestCase(TestCase):
    def test_table_block_autoescape(self):
        block = AskContent()
        data = block.to_python(
            [
                {
                    "type": "table_block",
                    "value": {
                        "data": [
                            [
                                "Column",
                                "<p>Column with HTML<br/></p>",
                            ],
                        ],
                        "has_data": True,
                    },
                },
            ]
        )
        expected_html = (
            '<div class="row table_block-row">'
            '<table class="o-table">'
            "<tbody>"
            "<tr><td>Column</td><td><p>Column with HTML<br/></p></td></tr>"
            "</tbody>"
            "</table>"
            "</div>"
        )
        html = block.render(data)
        self.assertHTMLEqual(html, expected_html)
