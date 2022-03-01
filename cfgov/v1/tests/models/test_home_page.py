from django.test import RequestFactory, SimpleTestCase

from v1.models.home_page import HighlightCardBlock, HomePage


class HomePageTests(SimpleTestCase):
    def test_highlight_card_block_rendering(self):
        block = HighlightCardBlock()
        value = block.to_python(
            {
                "heading": "Highlight",
                "text": "This is a highlight.",
                "link_url": "/highlight/",
            }
        )
        self.assertEqual(value.link_text, "Read more")

    def test_render(self):
        request = RequestFactory().get("/")
        page = HomePage(title="home", live=True)
        response = page.serve(request)
        self.assertEqual(response.template_name, "v1/home_page.html")
