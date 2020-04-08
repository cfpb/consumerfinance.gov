from django.test import TestCase, override_settings


try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


# Remove this file and the associated URLs and templates
# after the HMDA API is retired (hopefully summer 2019)
class LegacyHmdaPagesTest(TestCase):
    @override_settings(
        FLAGS={"HMDA_LEGACY_PUBLISH": [("boolean", True)]}
    )
    def test_legacy_explorer_after_publication(self):
        response = self.client.get(reverse("legacy_explorer_published"))
        self.assertEqual(response.status_code, 200)

    @override_settings(
        FLAGS={"HMDA_LEGACY_PUBLISH": [("boolean", False)]}
    )
    def test_legacy_explorer_disabled(self):
        response = self.client.get(reverse("legacy_explorer_published"))
        self.assertEqual(response.status_code, 404)
