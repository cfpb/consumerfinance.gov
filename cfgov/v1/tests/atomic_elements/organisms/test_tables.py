from django.test import SimpleTestCase

from v1.atomic_elements.tables import ContactUsTable


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
