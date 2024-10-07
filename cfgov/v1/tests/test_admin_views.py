from django.http import Http404, HttpRequest
from django.test import TestCase

from v1.admin_views import redirect_to_internal_docs
from v1.models import InternalDocsSettings


class InternalDocsViewTests(TestCase):
    def test_docs_not_defined_view_returns_404(self):
        with self.assertRaises(Http404):
            redirect_to_internal_docs(HttpRequest())

    def test_docs_defined_view_redirects_to_guide_url(self):
        InternalDocsSettings.objects.create(url="https://example.com/")
        response = redirect_to_internal_docs(HttpRequest())
        self.assertEqual(
            (response["Location"], response.status_code),
            ("https://example.com/", 302),
        )
