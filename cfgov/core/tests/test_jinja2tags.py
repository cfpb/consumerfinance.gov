import os
from unittest.mock import patch

from django.http import HttpRequest
from django.template import engines
from django.test import SimpleTestCase, TestCase, override_settings

from core.tests.templatetags.test_svg_icon import VALID_SVG


@override_settings(
    STATICFILES_DIRS=[
        os.path.join(os.path.dirname(__file__), "staticfiles"),
    ]
)
class SvgIconTests(TestCase):
    def setUp(self):
        self.jinja_engine = engines["wagtail-env"]

    def test_jinja_tag(self):
        template = self.jinja_engine.from_string('{{ svg_icon("test") }}')
        self.assertEqual(template.render(), VALID_SVG)

    @patch("core.templatetags.svg_icon.FALLBACK_ICON_NAME", "test")
    def test_jinja_tag_fallback(self):
        template = self.jinja_engine.from_string('{{ svg_icon("invalid") }}')
        self.assertEqual(template.render(), VALID_SVG)

    @patch("core.templatetags.svg_icon.FALLBACK_ICON_NAME", "missing")
    def test_jinja_tag_fallback_not_found_error(self):
        template = self.jinja_engine.from_string('{{ svg_icon("missing") }}')
        with self.assertRaises(FileNotFoundError):
            template.render()

    @patch("core.templatetags.svg_icon.FALLBACK_ICON_NAME", "invalid")
    def test_jinja_tag_fallback_invalid_error(self):
        template = self.jinja_engine.from_string('{{ svg_icon("invalid") }}')
        with self.assertRaises(ValueError):
            template.render()


@override_settings(FLAGS={"MY_FLAG": [("boolean", True)]})
class FeatureFlagTests(TestCase):
    def setUp(self):
        self.jinja_engine = engines["wagtail-env"]

    def test_flag_enabled_tag(self):
        template = self.jinja_engine.from_string(
            '{{ flag_enabled("MY_FLAG") }}'
        )
        self.assertEqual(template.render({"request": None}), "True")

    def test_flag_disabled_tag(self):
        template = self.jinja_engine.from_string(
            '{{ flag_disabled("MY_FLAG") }}'
        )
        self.assertEqual(template.render({"request": None}), "False")


class SlugifyUniqueTests(SimpleTestCase):
    def setUp(self):
        self.engine = engines["wagtail-env"]
        self.template = '{{ "Some text" | slugify_unique }}'

    def render(self, template, context=None):
        return self.engine.from_string(template).render(context=context)

    def test_no_context(self):
        self.assertEqual(self.render(self.template), "some-text")

    def test_no_request_in_context(self):
        self.assertEqual(self.render(self.template, {}), "some-text")

    def test_render_with_request_in_context(self):
        self.assertEqual(
            self.render(self.template, {"request": HttpRequest()}), "some-text"
        )

    def test_render_uses_request_to_make_multiple_unique_slugs(self):
        request = HttpRequest()
        template = " and ".join([self.template, self.template])
        self.assertEqual(
            self.render(template, {"request": request}),
            "some-text and some-text-1",
        )

    def test_render_without_request_repeats_slugs(self):
        template = " and ".join([self.template, self.template])
        self.assertEqual(self.render(template), "some-text and some-text")

    def test_multiple_renders_multiple_unique_slugs(self):
        request = HttpRequest()
        rendered = [
            self.render(self.template, {"request": request}) for _ in range(5)
        ]

        self.assertEqual(
            rendered,
            [
                "some-text",
                "some-text-1",
                "some-text-2",
                "some-text-3",
                "some-text-4",
            ],
        )

    def test_different_requests_allow_repeats(self):
        for _ in range(5):
            self.assertEqual(
                self.render(self.template, {"request": HttpRequest()}),
                "some-text",
            )
