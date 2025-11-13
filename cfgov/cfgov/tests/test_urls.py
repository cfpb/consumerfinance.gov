from unittest import mock

import django
from django.test import (
    RequestFactory,
    SimpleTestCase,
    TestCase,
    override_settings,
)
from django.urls import re_path

from cfgov import urls
from cfgov.urls.redirect_helpers import perm, temp
from cfgov.urls.views import (
    flagged_wagtail_only_view,
    flagged_wagtail_template_view,
)


try:
    from django.urls import URLPattern, URLResolver
except ImportError:
    from django.core.urlresolvers import RegexURLPattern as URLPattern
    from django.core.urlresolvers import RegexURLResolver as URLResolver


# Allowlist is a list of *strings* that match the beginning of a regex string.
# For example, ''^admin' will match any urlpattern regex that starts with
# '^admin'.
ADMIN_URL_ALLOWLIST = [
    "^admin/",
    "^csp-report/",
    "^d/admin/",
    "^django-admin/",
    "^login",
    "^logout",
    "^oidc/",
    "^password/",
    "^tasks/",
]


# Based on django_extensions's show_urls command.
def extract_regexes_from_urlpatterns(urlpatterns, base=""):
    """Extract a list of all regexes from the given urlpatterns"""
    regexes = []
    for p in urlpatterns:
        if isinstance(p, URLPattern) or hasattr(p, "_get_callback"):
            if django.VERSION < (2, 0):
                regexes.append(base + p.regex.pattern)
            else:
                regexes.append(base + p.pattern.regex.pattern)
        elif (
            isinstance(p, URLResolver)
            or hasattr(p, "url_patterns")
            or hasattr(p, "_get_url_patterns")
        ):
            patterns = p.url_patterns
            if django.VERSION < (2, 0):
                regexes.extend(
                    extract_regexes_from_urlpatterns(
                        patterns, base + p.regex.pattern
                    )
                )
            else:
                regexes.extend(
                    extract_regexes_from_urlpatterns(
                        patterns, base + p.pattern.regex.pattern
                    )
                )
        else:
            raise TypeError(f"{p} does not appear to be a urlpattern object")
    return regexes


urlpatterns = [
    flagged_wagtail_only_view("MY_TEST_FLAG", r"^$"),
    re_path(
        "^template$",
        flagged_wagtail_template_view(
            "MY_TEST_FLAG",
            "tccp/about.html",
        ),
    ),
]


@override_settings(ROOT_URLCONF=__name__)
class FlaggedWagtailViewTests(TestCase):
    @override_settings(FLAGS={"MY_TEST_FLAG": [("boolean", True)]})
    def test_flag_set_returns_view_that_calls_wagtail_serve_view(self):
        """When flag is set, request should be routed to Wagtail.

        This test checks for text that is known to exist in the template for
        the Wagtail page that gets served from the site root.
        """
        response = self.client.get("/")
        self.assertContains(response, "Consumer Financial Protection Bureau")

    @override_settings(FLAGS={"MY_TEST_FLAG": [("boolean", False)]})
    def test_flag_not_set_returns_view_that_raises_http404(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 404)

        response = self.client.get("/template")
        self.assertContains(response, "About this tool")


class HandleErrorTestCase(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")

    def test_handle_error(self):
        with mock.patch("cfgov.urls.views.render") as mock_render:
            urls.handle_error(404, self.request)

        mock_render.assert_called_with(
            self.request,
            "v1/layouts/404.html",
            context={"request": self.request},
            status=404,
        )

    def test_error_while_handling_404_should_be_raised(self):
        with mock.patch(
            "cfgov.urls.views.render", side_effect=RuntimeError
        ), self.assertRaises(RuntimeError):
            urls.handler404(self.request)

    def test_error_while_handling_500_should_log_plain_text_response(self):
        with mock.patch("cfgov.urls.views.render", side_effect=RuntimeError):
            result = urls.handler500(self.request)
            self.assertIn(
                b"This request could not be processed", result.content
            )
            self.assertIn(b"HTTP Error 500.", result.content)


class TestBetaRefreshEndpoint(TestCase):
    def test_beta_testing_endpoint_returns_404_when_disabled(self):
        response = self.client.get("/beta_external_testing/")
        self.assertEqual(response.status_code, 404)

    @override_settings(FLAGS={"BETA_EXTERNAL_TESTING": [("boolean", True)]})
    def test_beta_testing_endpoint_returns_200_when_enabled(self):
        response = self.client.get("/beta_external_testing/")
        self.assertEqual(response.status_code, 200)

    @override_settings(FLAGS={"BETA_EXTERNAL_TESTING": [("boolean", True)]})
    def test_beta_testing_endpoint_is_no_cache_when_enabled(self):
        response = self.client.get("/beta_external_testing/")
        self.assertEqual(response["Akamai-Cache-Control"], "no-store")


class RedirectHelperTests(SimpleTestCase):
    def setUp(self):
        self.redirects = []

    def test_perm(self):
        pattern = perm(r"old", "new", append_to=self.redirects)
        self.assertEqual(self.redirects, [pattern])
        self.assertEqual(pattern.pattern.regex.pattern, "^old$")
        self.assertTrue(pattern.callback.view_initkwargs["permanent"])

    def test_temp(self):
        pattern = temp(r"old", "new", append_to=self.redirects)
        self.assertEqual(self.redirects, [pattern])
        self.assertEqual(pattern.pattern.regex.pattern, "^old$")
        self.assertFalse(pattern.callback.view_initkwargs["permanent"])


class TestAFewRedirects(SimpleTestCase):
    def test_redirects(self):
        for url, code, target in [
            (
                "/f/foo/bar?baz=1",
                302,
                "https://files.consumerfinance.gov/f/foo/bar",
            ),
            (
                "/payments/foo/bar",
                301,
                "/enforcement/payments-harmed-consumers/payments-by-case/foo/bar",
            ),
            (
                "/eregulations/a/b/c/2015-26607_20180101/d/e/f",
                302,
                "/eregulations/a/b/c/2017-18284_20180101/d/e/f",
            ),
            (
                "/policy-compliance/guidance/consumer-cards-resources/foo/bar",
                301,
                "/compliance/consumer-cards-resources/foo/bar",
            ),
            (
                "/blog/category/jobs/foo/bar",
                301,
                "/about-us/blog/?filter1_topics=careers",
            ),
            (
                "/owning-a-home/process/foo/bar",
                301,
                "/owning-a-home/foo/bar",
            ),
            (
                "/rules-policy/regulations/1234/5678/foo/bar",
                301,
                "/rules-policy/regulations/5678/foo/bar",
            ),
            (
                "/leadership-calendar/",
                301,
                "/about-us/the-bureau/leadership-calendar/",
            ),
        ]:
            with self.subTest(url=url, code=code, target=target):
                response = self.client.get(url)
                self.assertEqual(response.status_code, code)
                self.assertEqual(response["Location"], target)
