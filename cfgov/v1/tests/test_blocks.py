from unittest import mock

from django.core.exceptions import ValidationError
from django.test import TestCase

from v1.blocks import AnchorLink, EscapedHTMLValidator, UnescapedRichTextBlock


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


class EscapedHTMLValidatorTestCase(TestCase):
    def test_disallowed_elements(self):
        validator = EscapedHTMLValidator(
            allowed_elements=(
                "svg",
                "path",
            )
        )
        value = (
            "Velit doloremque modi dolorum ducimus nesciunt harum. "
            "Enim voluptatum animi dolorem aspernatur consequuntur &lt;br&gt;"
            "&lt;svg xmlns=&quot;http://www.w3.org/2000/svg&quot; "
            "viewBox=&quot;0 0 100 100&quot;&gt;"
            "&lt;path d=&quot;M 50,50&quot;&gt;&lt;/path&gt;&lt;/svg&gt;"
            "&lt;h2&gt;Asperiores nesciunt fugit sint qui ut culpa.&lt;/h2&gt;"
        )

        with self.assertRaises(ValidationError) as cm:
            validator(value)

        self.assertIn(
            "Invalid HTML element(s) found: br, h2", cm.exception.message
        )
        self.assertIn(
            "The only HTML elements allowed are svg, path.",
            cm.exception.message,
        )


class UnescapedRichTextBlockTestCase(TestCase):
    def test_to_python_with_entities(self):
        block = UnescapedRichTextBlock()
        value = "Neque porro &lt;i&gt;quisquam&lt;/i&gt; est qui dolorem ipsum"
        rich_text = block.to_python(value)
        self.assertEqual(
            rich_text.source,
            "Neque porro <i>quisquam</i> est qui dolorem ipsum",
        )
