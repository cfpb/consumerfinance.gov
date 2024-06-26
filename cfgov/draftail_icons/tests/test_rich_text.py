import json
from unittest.mock import patch

from django.test import SimpleTestCase

from wagtail.admin.rich_text.converters.contentstate import (
    ContentstateConverter,
)

from draftjs_exporter.dom import DOM

from core.tests.templatetags.test_svg_icon import VALID_SVG
from draftail_icons.rich_text import (
    IconEntityElementHandler,
    icon_entity_decorator,
)


class IconEntityDecoratorTestCase(SimpleTestCase):
    @patch("draftail_icons.rich_text.svg_icon")
    def test_icon_entity_decorator(self, mock_svg_icon):
        mock_svg_icon.return_value = VALID_SVG
        result = icon_entity_decorator(
            {"icon-name": "piggy-bank", "children": " "}
        )
        html = DOM.render(result)
        self.assertEqual(
            html, f'<span data-icon-name="piggy-bank">{VALID_SVG}</span>'
        )


class IconEntityElementHandlerTestCase(SimpleTestCase):
    def setUp(self):
        self.converter = ContentstateConverter(features=["icon"])
        self.handler = IconEntityElementHandler("ICON")

    def test_get_attribute_data(self):
        attribute_data = self.handler.get_attribute_data(
            {"data-icon-name": "piggy-bank"}
        )
        self.assertIn("icon-name", attribute_data)
        self.assertEqual(attribute_data["icon-name"], "piggy-bank")

    def test_handle_endtag(self):
        html = f"""
            <p data-block-key='00000'>
            Do some
            <span data-icon-name="piggy-bank">{VALID_SVG}</span>
            banking!
            </p>
        """
        result = json.loads(self.converter.from_database_format(html))
        self.assertEqual(result["entityMap"]["0"]["type"], "ICON")
        self.assertEqual(result["blocks"][0]["entityRanges"][0]["length"], 1)
