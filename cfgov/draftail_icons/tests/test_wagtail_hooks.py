from django.test import SimpleTestCase

from wagtail.rich_text import features as feature_registry


class WagtailHooksestCase(SimpleTestCase):
    def test_register_icon_feature(self):
        self.assertIn("icon", feature_registry.plugins_by_editor["draftail"])
        self.assertIsNotNone(
            feature_registry.get_converter_rule("contentstate", "icon")
        )
