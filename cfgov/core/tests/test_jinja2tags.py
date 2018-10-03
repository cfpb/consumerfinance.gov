import os

from django.template import engines
from django.test import TestCase, override_settings

from core.tests.templatetags.test_svg_icon import VALID_SVG


@override_settings(
    STATICFILES_DIRS=[
        os.path.join(os.path.dirname(__file__), 'staticfiles'),
    ]
)
class SvgIconTests(TestCase):
    def setUp(self):
        self.jinja_engine = engines['wagtail-env']

    def test_jinja_tag(self):
        template = self.jinja_engine.from_string('{{ svg_icon("test") }}')
        self.assertEqual(template.render(), VALID_SVG)

    def test_jinja_tag_invalid(self):
        template = self.jinja_engine.from_string('{{ svg_icon("invalid") }}')
        with self.assertRaises(ValueError):
            template.render()


@override_settings(FLAGS={'MY_FLAG': {'boolean': 'True'}})
class FeatureFlagTests(TestCase):
    def setUp(self):
        self.jinja_engine = engines['wagtail-env']

    def test_flag_enabled_tag(self):
        template = self.jinja_engine.from_string(
            '{{ flag_enabled("MY_FLAG") }}'
        )
        self.assertEqual(template.render({'request': None}), 'True')

    def test_flag_disabled_tag(self):
        template = self.jinja_engine.from_string(
            '{{ flag_disabled("MY_FLAG") }}'
        )
        self.assertEqual(template.render({'request': None}), 'False')
