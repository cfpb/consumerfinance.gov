import os

from django.template import engines
from django.test import TestCase, override_settings

from core.tests.templatetags.test_svg_icon import VALID_SVG


@override_settings(
    STATICFILES_DIRS=[
        os.path.join(os.path.dirname(__file__), 'staticfiles'),
    ],
    TEMPLATES=[
        {
            'NAME': 'test',
            'BACKEND': 'django.template.backends.jinja2.Jinja2',
            'OPTIONS': {
                'extensions': [
                    'core.jinja2tags.filters',
                ],
            },
        },
    ]
)
class SvgIconTests(TestCase):
    def setUp(self):
        self.jinja_engine = engines['test']

    def test_jinja_tag(self):
        template = self.jinja_engine.from_string('{{ svg_icon("test") }}')
        self.assertEqual(template.render(), VALID_SVG)

    def test_jinja_tag_invalid(self):
        template = self.jinja_engine.from_string('{{ svg_icon("invalid") }}')
        with self.assertRaises(ValueError):
            template.render()
