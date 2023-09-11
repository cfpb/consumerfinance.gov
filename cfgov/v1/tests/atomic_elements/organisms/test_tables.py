from django.test import SimpleTestCase
from django.utils.html import escape

from v1.atomic_elements.tables import ContactUsTable, TableAdapter


class ContactUsTableTests(SimpleTestCase):
    def test_disallows_unsafe_content(self):
        block = ContactUsTable()
        value = block.to_python(
            {
                "rows": [
                    {
                        "title": "<script>alert('title')</script>",
                        "body": escape("<script>alert('body')</script>"),
                    }
                ],
            }
        )
        html = block.render(value)

        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)


class TableTests(SimpleTestCase):
    def test_table_adapter_media(self):
        media = TableAdapter().media
        self.assertFalse(media._css)
        self.assertIn("apps/admin/js/table.js", media._js)
