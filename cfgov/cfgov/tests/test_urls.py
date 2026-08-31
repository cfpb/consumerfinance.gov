from django.test import SimpleTestCase, TestCase, override_settings


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
