from django.core.exceptions import ImproperlyConfigured
from django.test import RequestFactory, SimpleTestCase

from v1.views.template_debug import TemplateDebugView


class TemplateDebugViewTests(SimpleTestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")

    def test_misconfigured_without_parameters(self):
        with self.assertRaises(ImproperlyConfigured):
            TemplateDebugView.as_view()(self.request)

    def test_renders_debug_template_name(self):
        debug_template_name = "_includes/atoms/hyperlink.html"

        view = TemplateDebugView.as_view(
            debug_template_name=debug_template_name, debug_test_cases={}
        )
        response = view(self.request)

        self.assertContains(response, debug_template_name)

    def test_renders_debug_template_with_test_cases(self):
        test_cases = {
            "First": {
                "url": "https://example.com/first/",
                "text": "First test case to be rendered",
            },
            "Second": {
                "url": "https://example.com/second/",
                "text": "Second test case to be rendered",
            },
        }

        view = TemplateDebugView.as_view(
            debug_template_name="_includes/atoms/hyperlink.html",
            debug_test_cases=test_cases,
        )

        response = view(self.request)

        # The view should render the provided template (the hyperlink atom)
        # with each of the test cases.
        for _, test_case in test_cases.items():
            self.assertContains(response, f'href="{test_case["url"]}"')

    def test_renders_extra_js(self):
        debug_template_name = "_includes/atoms/hyperlink.html"

        view = TemplateDebugView.as_view(
            debug_template_name=debug_template_name,
            debug_test_cases={},
            extra_js=["template-debug-extra.js"],
        )
        response = view(self.request)

        self.assertContains(response, "template-debug-extra.js")
