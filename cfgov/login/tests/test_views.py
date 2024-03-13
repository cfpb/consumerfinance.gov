from unittest import mock

from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, TestCase
from django.urls import reverse

from login.views import lockout


class TestLockoutView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.session_middleware = SessionMiddleware(mock.MagicMock())
        self.messages_middleware = MessageMiddleware(mock.MagicMock())

    def test_lockout_view_redirects(self):
        request = self.factory.post("/admin/login")
        self.session_middleware.process_request(request)
        self.messages_middleware.process_request(request)
        response = lockout(request, None)
        # Because this response is from calling the view directly, not from
        # Django's test client, we can't use assertRedirects, which checks
        # for the client instance on the response object.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.headers["Location"], reverse("wagtailadmin_login")
        )
