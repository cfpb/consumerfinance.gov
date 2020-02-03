import json

from django.template import engines
from django.test import (
    RequestFactory, SimpleTestCase, TestCase, override_settings
)

from mega_menu.models import Menu


class MegaMenuTemplateTests(SimpleTestCase):
    def render_template_name(self):
        jinja_engine = engines['wagtail-env']
        template = jinja_engine.from_string('{{ mega_menu_template() }}')
        return template.render()

    @override_settings(FLAGS={})
    def test_default_template(self):
        self.assertEqual(
            self.render_template_name(),
            '_includes/organisms/mega-menu.html'
        )

    @override_settings(FLAGS={'MEGA_MENU_VAR_1': [('boolean', True)]})
    def test_template_variation_1(self):
        self.assertEqual(
            self.render_template_name(),
            '_includes/organisms/mega-menu-var-1.html'
        )

    @override_settings(FLAGS={'MEGA_MENU_VAR_2': [('boolean', True)]})
    def test_template_variation_2(self):
        self.assertEqual(
            self.render_template_name(),
            '_includes/organisms/mega-menu-var-2.html'
        )


class MegaMenuTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Menu.objects.create(language='en', submenus=json.dumps([
            {'type': 'submenu', 'value': {'title': 'English'}},
        ]))

        Menu.objects.create(language='es', submenus=json.dumps([
            {'type': 'submenu', 'value': {'title': 'Spanish'}},
        ]))

    def render_mega_menu(self, context):
        jinja_engine = engines['wagtail-env']
        template = jinja_engine.from_string('{{ mega_menu() }}')
        return template.render(context)

    def test_empty_context_fails_due_to_missing_response(self):
        with self.assertRaises(KeyError):
            self.render_mega_menu({})

    def test_uses_request_falls_back_to_default_language(self):
        request = RequestFactory().get('/')
        html = self.render_mega_menu({'request': request})
        self.assertIn('English', html)

    def test_uses_request_language_if_set(self):
        request = RequestFactory().get('/', HTTP_ACCEPT_LANGUAGE='es')
        html = self.render_mega_menu({'request': request})
        self.assertIn('Spanish', html)

    def test_unsupported_language_falls_back_to_default_language(self):
        request = RequestFactory().get('/', HTTP_ACCEPT_LANGUAGE='fr')
        html = self.render_mega_menu({'request': request})
        self.assertIn('English', html)

    def test_uses_language_from_context_instead_of_request(self):
        request = RequestFactory().get('/', HTTP_ACCEPT_LANGUAGE='en')
        html = self.render_mega_menu({'request': request, 'language': 'es'})
        self.assertIn('Spanish', html)

    def test_unsupported_language_in_context_falls_back_to_default(self):
        request = RequestFactory().get('/')
        html = self.render_mega_menu({'request': request, 'language': 'fr'})
        self.assertIn('English', html)

    def test_renders_in_single_database_query(self):
        request = RequestFactory().get('/')
        with self.assertNumQueries(1):
            self.render_mega_menu({'request': request})
