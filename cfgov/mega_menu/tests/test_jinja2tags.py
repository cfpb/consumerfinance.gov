import json

from django.test import RequestFactory, TestCase

from mega_menu.jinja2tags import get_mega_menu_content
from mega_menu.models import Menu


class MegaMenuTests(TestCase):
    def setUp(self):
        Menu.objects.create(
            language="en",
            submenus=json.dumps(
                [
                    {"type": "submenu", "value": {"title": "English"}},
                ]
            ),
        )

        Menu.objects.create(
            language="es",
            submenus=json.dumps(
                [
                    {"type": "submenu", "value": {"title": "Spanish"}},
                ]
            ),
        )

    def test_returns_none_if_no_menus_exist(self):
        Menu.objects.all().delete()

        request = RequestFactory().get("/")
        self.assertIsNone(get_mega_menu_content({"request": request}))

    def test_empty_context_falls_back_to_default_language(self):
        content = get_mega_menu_content({})
        self.assertIn("English", json.dumps(content))

    def test_ignores_request_falls_back_to_default_language(self):
        request = RequestFactory().get("/")
        content = get_mega_menu_content({"request": request})
        self.assertIn("English", json.dumps(content))

    def test_ignores_request_language_if_set(self):
        request = RequestFactory().get("/", HTTP_ACCEPT_LANGUAGE="es")
        content = get_mega_menu_content({"request": request})
        self.assertIn("English", json.dumps(content))

    def test_uses_language_from_context_instead_of_request(self):
        request = RequestFactory().get("/")
        content = get_mega_menu_content({"request": request, "language": "es"})
        self.assertIn("Spanish", json.dumps(content))

    def test_unsupported_language_in_context_falls_back_to_default(self):
        request = RequestFactory().get("/")
        content = get_mega_menu_content({"request": request, "language": "fr"})
        self.assertIn("English", json.dumps(content))

    def test_renders_in_single_database_query(self):
        request = RequestFactory().get("/")
        with self.assertNumQueries(1):
            get_mega_menu_content({"request": request})
