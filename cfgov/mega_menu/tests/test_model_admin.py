import json

from django.test import TestCase

from wagtail.tests.utils import WagtailTestUtils

from mega_menu.models import Menu


class ModelAdminTests(TestCase, WagtailTestUtils):
    def setUp(self):
        self.login()

    @classmethod
    def setUpTestData(cls):
        submenus = json.dumps(
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

        Menu.objects.bulk_create(
            [
                Menu(language=language, submenus=submenus)
                for language in ("en", "es")
            ]
        )

    def test_index_view_contains_preview_button(self):
        response = self.client.get("/admin/mega_menu/menu/")
        self.assertContains(response, "Preview this menu")

    def test_preview_view(self):
        response = self.client.get("/admin/mega_menu/menu/preview/en/")
        self.assertContains(response, "Test column heading")

    def test_preview_view_renders_using_correct_language(self):
        response = self.client.get("/admin/mega_menu/menu/preview/en/")
        self.assertContains(response, "An official website")
        self.assertNotContains(response, "Un sitio web oficial")

        response = self.client.get("/admin/mega_menu/menu/preview/es/")
        self.assertNotContains(response, "An official website")
        self.assertContains(response, "Un sitio web oficial")
