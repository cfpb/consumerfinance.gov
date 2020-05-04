from django.test import TestCase
from django.urls import reverse


class TestTokenProviderView(TestCase):
    def setUp(self):
        self.url = reverse("csrf-token-provider")

    def test_get_returns_plain_http_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_returns_csrf_token(self):
        response = self.client.post(self.url)
        self.assertTemplateUsed(response, "common/csrf.html")

    def test_post_marks_session_as_modified(self):
        response = self.client.post(self.url)
        self.assertTrue(response.wsgi_request.session.modified)
