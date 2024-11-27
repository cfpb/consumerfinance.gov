from django.test import TestCase

from wagtail.models import Site

from v1.atomic_elements.charts import CHART_COLORS, CHART_TYPES, ChartBlock


class ChartBlockTestCase(TestCase):
    def setUp(self):
        self.root = Site.objects.get(is_default_site=True).root_page

    def test_chartblock_overrides(self):
        block = ChartBlock()

        # We override the chart types and colors
        self.assertEqual(block.chart_types, CHART_TYPES)
        self.assertEqual(block.meta.colors, CHART_COLORS)

        # And we override the child block ordering to ensure these are the
        # last three blocks in the editor.
        self.assertEqual(list(block.child_blocks.keys())[-1], "settings")
        self.assertEqual(list(block.child_blocks.keys())[-2], "datasets")
        self.assertEqual(list(block.child_blocks.keys())[-3], "chart_type")
