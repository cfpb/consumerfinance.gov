from unittest import mock

from django.test import TestCase

from v1.blocks import AnchorLink


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
