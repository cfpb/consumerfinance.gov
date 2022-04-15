import os.path

from django.template import engines
from django.template.loader import get_template
from django.test import TestCase, override_settings


@override_settings(
    TEMPLATES=[
        {
            "NAME": "test",
            "BACKEND": "django.template.backends.jinja2.Jinja2",
            "DIRS": [
                os.path.join(os.path.dirname(__file__), "templates"),
            ],
            "OPTIONS": {
                "environment": "v1.jinja2_environment.environment",
                "extensions": [
                    "jinja2.ext.i18n",
                ],
            },
        }
    ]
)
class RelativeTemplatePathTests(TestCase):
    def test_template_includes_use_relative_paths(self):
        expected = """
include "include.html": include from foo/bar
include "bar/include.html": include from foo/bar
include "foo/bar/include.html": include from foo/bar
include "/include.html": include from template root
""".strip()

        self.assertEqual(get_template("foo/bar/test.html").render(), expected)


class TranslationsTests(TestCase):
    def setUp(self):
        self.jinja2_engine = engines["wagtail-env"]

    def test_trans_statement(self):
        tmpl = self.jinja2_engine.from_string("{% trans %}foo{% endtrans %}")
        self.assertEqual(tmpl.render(), "foo")

    def test_underscore_syntax(self):
        tmpl = self.jinja2_engine.from_string('{{ _("foo") }}')
        self.assertEqual(tmpl.render(), "foo")

    def test_gettext(self):
        tmpl = self.jinja2_engine.from_string('{{ gettext("foo") }}')
        self.assertEqual(tmpl.render(), "foo")

    def test_ngettext(self):
        tmpl = self.jinja2_engine.from_string(
            '{{ ngettext("%(num)d item", "%(num)d items", items) }}'
        )
        self.assertEqual(tmpl.render({"items": 1}), "1 item")
        self.assertEqual(tmpl.render({"items": 3}), "3 items")
