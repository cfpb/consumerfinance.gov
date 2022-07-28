from unittest import mock

from django.test import TestCase
from django.utils.safestring import SafeText

from v1.blocks import AnchorLink, PlaceholderCharBlock, RAFToolBlock


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


class TestPlaceholderBlock(TestCase):
    def setUp(self):
        self.char_block = PlaceholderCharBlock()
        self.placeholder = PlaceholderCharBlock(placeholder="Hi there!")

    def test_render_no_placeholder_provided(self):
        html = self.char_block.render_form("Hello world!")
        self.assertInHTML(
            (
                '<input id="" name="" placeholder="" '
                'type="text" value="Hello world!" />'
            ),
            html,
        )

    def test_render_no_placeholder_returns_safetext(self):
        html = self.char_block.render_form("Hello world!")
        self.assertIsInstance(html, SafeText)

    def test_render_with_placeholder(self):
        html = self.placeholder.render_form("Hello world!")
        self.assertIn(
            (
                '<input id="" name="" placeholder="Hi there!" '
                'type="text" value="Hello world!"/>'
            ),
            html,
        )

    def test_render_returns_safetext(self):
        html = self.placeholder.render_form("Hello world!")
        self.assertIsInstance(html, SafeText)

    def test_replace_placeholder(self):
        html = '<input id="foo" placeholder="a" />'
        replaced = PlaceholderCharBlock.replace_placeholder(html, "b")
        self.assertEqual(replaced, '<input id="foo" placeholder="b"/>')

    def test_replace_placeholder_quotes(self):
        html = '<input id="foo" placeholder="&quot;a&quot;" />'
        replaced = PlaceholderCharBlock.replace_placeholder(html, '"b"')
        self.assertEqual(replaced, '<input id="foo" placeholder=\'"b"\'/>')

    def test_replace_placeholder_no_placeholder(self):
        html = '<input id="foo" />'
        replaced = PlaceholderCharBlock.replace_placeholder(html, "a")
        self.assertEqual(replaced, '<input id="foo" placeholder="a"/>')

    def test_no_inputs_raises_valueerror(self):
        html = "<div>something</div>"
        with self.assertRaises(ValueError):
            PlaceholderCharBlock.replace_placeholder(html, "a")

    def test_multiple_inputs_raises_valueerror(self):
        html = '<input id="foo" /><input id="bar" />'
        with self.assertRaises(ValueError):
            PlaceholderCharBlock.replace_placeholder(html, "a")


class RAFToolBlockTestCase(TestCase):
    def test_render_no_placeholder_provided(self):
        erap_tool_block = RAFToolBlock()
        html = erap_tool_block.render(None)
        self.assertInHTML(
            '<div id="rental-assistance-finder" data-language="en"></div>',
            html,
        )
