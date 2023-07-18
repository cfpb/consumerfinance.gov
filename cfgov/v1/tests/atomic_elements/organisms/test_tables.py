from django.test import SimpleTestCase, TestCase

from v1.atomic_elements.tables import ContactUsTable, RichTextTableInput


class TestRichTextTableInput(TestCase):
    def test_rich_text_table_js_included(self):
        self.assertIn(
            "apps/admin/js/rich-text-table.js", RichTextTableInput().media._js
        )


class ContactUsTableTests(SimpleTestCase):
    def test_disallows_unsafe_content(self):
        block = ContactUsTable()
        value = block.to_python(
            {
                "rows": [
                    {
                        "title": "<script>alert('title')</script>",
                        "body": "<script>alert('body')</script>",
                    }
                ],
            }
        )
        html = block.render(value)

        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)
