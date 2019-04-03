from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings


# Remove this file and the associated URLs and templates
# after the HMDA API is retired (hopefully summer 2019)
class LegacyHmdaPagesTest(TestCase):

    @override_settings(FLAGS={
        'HMDA_LEGACY_REVIEW': [('boolean', True)],
        'HMDA_LEGACY_PUBLISH': [('boolean', False)],
    })
    def test_legacy_explorer_review_phase(self):
        response = self.client.get(reverse('legacy_explorer_draft'))
        self.assertEqual(response.status_code, 200)

        response2 = self.client.get(reverse('legacy_explorer_published'))
        self.assertEqual(response2.status_code, 404)

    @override_settings(FLAGS={
        'HMDA_LEGACY_REVIEW': [('boolean', False)],
        'HMDA_LEGACY_PUBLISH': [('boolean', True)],
    })
    def test_legacy_explorer_after_publication(self):
        response = self.client.get(reverse('legacy_explorer_published'))
        self.assertEqual(response.status_code, 200)

        response2 = self.client.get(reverse('legacy_explorer_draft'))
        self.assertEqual(response2.status_code, 404)

    @override_settings(FLAGS={
        'HMDA_LEGACY_REVIEW': [('boolean', False)],
        'HMDA_LEGACY_PUBLISH': [('boolean', False)],
    })
    def test_legacy_explorer_disabled(self):
        response = self.client.get(reverse('legacy_explorer_published'))
        self.assertEqual(response.status_code, 404)

        response2 = self.client.get(reverse('legacy_explorer_draft'))
        self.assertEqual(response2.status_code, 404)
