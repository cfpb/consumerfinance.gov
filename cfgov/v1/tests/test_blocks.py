import json
import uuid
from unittest import mock

from django.test import RequestFactory, TestCase

from wagtail.models import Site

from wagtail_footnotes.models import Footnote

from v1.blocks import AnchorLink, RichTextBlockWithFootnotes
from v1.models import DocumentDetailPage


class TestAnchorLink(TestCase):
    def setUp(self):
        self.block = AnchorLink()

    def stringContainsNumbers(self, string):
        return any(char.isdigit() for char in string)

    @mock.patch("v1.blocks.AnchorLink.clean")
    def test_clean_calls_format_id(self, mock_format_id):
        self.data = {"link_id": "test-string"}
        self.block.clean(self.data)
        self.assertTrue(mock_format_id.called)

    def test_clean_called_with_empty_data(self):
        self.data = {"link_id": ""}
        result = self.block.clean(self.data)
        prefix, suffix = result["link_id"].split("_")

        assert "anchor_" in result["link_id"]
        assert prefix == "anchor"
        assert self.stringContainsNumbers(suffix)

    def test_clean_called_with_string(self):
        self.data = {"link_id": "kittens playing with string"}
        result = self.block.clean(self.data)
        assert "anchor_kittens-playing-with-string_" in result["link_id"]

    def test_clean_called_with_existing_anchor(self):
        self.data = {"link_id": "anchor_3472e83b2dd084"}
        result = self.block.clean(self.data)
        assert result["link_id"] == "anchor_3472e83b2dd084"

    def test_clean_called_with_literally_anchor(self):
        self.data = {"link_id": "anchor"}
        result = self.block.clean(self.data)

        assert "anchor_" in result["link_id"]
        assert self.stringContainsNumbers(result["link_id"])


class RichTextBlockWithFootnotesTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.root_page = Site.objects.get(is_default_site=True).root_page

        footnote_uuid = uuid.uuid4()
        self.page = DocumentDetailPage(
            title="Test page",
            content=json.dumps(
                [
                    {
                        "type": "full_width_text",
                        "value": [
                            {
                                "type": "content_with_footnotes",
                                "value": (
                                    "<p>Test with note<footnote "
                                    f'id="{footnote_uuid}">1</footnote></p>'
                                ),
                            }
                        ],
                    }
                ]
            ),
        )
        self.root_page.add_child(instance=self.page)
        self.page.save_revision().publish()
        self.footnote = Footnote.objects.create(
            uuid=footnote_uuid,
            page=self.page,
            text="Test footnote",
        )

    def test_render_footnote_tag(self):
        block = RichTextBlockWithFootnotes()
        html = block.render_footnote_tag(2)
        self.assertHTMLEqual(
            html,
            '<a aria-labelledby="footnotes" href="#footnote-2" '
            'id="footnote-source-2"><sup>2</sup></a>',
        )

    def test_block_replace_footnote_tags_no_notes(self):
        block = RichTextBlockWithFootnotes()
        html = block.replace_footnote_tags(None, "foo")
        self.assertEqual(html, "foo")

    def test_block_replace_footnote_tags(self):
        rich_text_with_footnotes = self.page.content.stream_block.child_blocks[
            "full_width_text"
        ].child_blocks["content_with_footnotes"]
        value = rich_text_with_footnotes.get_prep_value(
            self.page.content[0].value[0].value
        )
        request = self.factory.get("/test-page/")
        context = self.page.get_context(request)
        result = rich_text_with_footnotes.render(value, context=context)
        self.assertEqual(
            result,
            '<p>Test with note<a aria-labelledby="footnotes" '
            'href="#footnote-1" id="footnote-source-1"><sup>1</sup></a></p>',
        )
