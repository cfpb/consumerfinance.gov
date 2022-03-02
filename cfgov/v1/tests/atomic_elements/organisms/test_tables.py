from django.test import TestCase

from wagtail.core.models import Site
from wagtail.tests.testapp.models import SimplePage

from v1.atomic_elements.organisms import (
    AtomicTableBlock,  # import from organisms for import check
)
from v1.atomic_elements.tables import RichTextTableInput


class TestRichTextTableInput(TestCase):
    def test_rich_text_table_js_included(self):
        self.assertIn(
            "apps/admin/js/rich-text-table.js", RichTextTableInput().media._js
        )


class TestAtomicTableBlock(TestCase):
    def test_render_with_data(self):
        value = {"data": [["Header 1", "Header 2"], ["1", "2"]]}
        block = AtomicTableBlock()
        result = block.render(value)
        self.assertIn("<table", result)

    def test_render_rich_text_page_links_expanded(self):
        page = SimplePage(title="title", slug="slug", content="content")
        default_site = Site.objects.get(is_default_site=True)
        default_site.root_page.add_child(instance=page)

        value = {
            "data": [['<a linktype="page" id="{}">'.format(page.pk)]],
        }
        block = AtomicTableBlock()
        result = block.render(value)
        self.assertIn('href="/slug/"', result)

    def test_render_header_with_unicode_characters(self):
        value = {
            "data": [["H\xebader 1", "Header 2"], ["1", "2"]],
            "first_row_is_table_header": True,
            "is_stacked": True,
        }
        block = AtomicTableBlock()
        result = block.render(value)
        self.assertIn("H\xebader", result)

    def test_get_field(self):
        block = AtomicTableBlock()
        field = block.field
        self.assertEqual(field.widget.__class__, RichTextTableInput)
