import json

from django.test import RequestFactory, TestCase

from mega_menu.models import Menu


class MenuTests(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        self.submenus = json.dumps(
            [
                {
                    "type": "submenu",
                    "value": {
                        "columns": [
                            {
                                "heading": "Test column heading",
                                "links": [
                                    {
                                        "url": "/foo/bar/",
                                        "text": "Test menu link",
                                    },
                                ],
                            },
                        ],
                    },
                }
            ]
        )

    def test_str(self):
        self.assertEqual(str(Menu("en")), "English")
        self.assertEqual(str(Menu("es")), "Spanish")

    def test_serve_preview_en(self):
        menu = Menu("en", submenus=self.submenus)
        response = menu.serve_preview(self.request, mode_name="default")
        self.assertContains(response, "An official website")
        self.assertNotContains(response, "Un sitio web oficial")

    def test_serve_preview_es(self):
        menu = Menu("es", submenus=self.submenus)
        response = menu.serve_preview(self.request, mode_name="default")
        self.assertNotContains(response, "An official website")
        self.assertContains(response, "Un sitio web oficial")
