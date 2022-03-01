from unittest.mock import patch

from django.contrib.auth.models import User
from django.core import mail
from django.http import HttpRequest
from django.test import TestCase

from wagtail.core.models import Site

from login.email import create_request_for_email, send_password_reset_email
from model_bakery import baker


class CreateEmailRequestTestCase(TestCase):
    def test_no_sites_raises_exception(self):
        with patch("login.email.Site.objects.get", side_effect=Site.DoesNotExist):
            self.assertRaises(RuntimeError, create_request_for_email)

    def assertRequestMatches(self, request, hostname, port, is_secure):
        self.assertEqual(
            (hostname, port, is_secure),
            (
                request.META["SERVER_NAME"],
                request.META["SERVER_PORT"],
                request.is_secure(),
            ),
        )

    def test_http_site(self):
        site = baker.prepare(Site, is_default_site=True, port=80)
        with patch("login.email.Site.objects.get", return_value=site):
            request = create_request_for_email()
        self.assertRequestMatches(request, site.hostname, site.port, False)

    def test_https_site(self):
        site = baker.prepare(Site, is_default_site=True, port=443)
        with patch("login.email.Site.objects.get", return_value=site):
            request = create_request_for_email()
        self.assertRequestMatches(request, site.hostname, site.port, True)


class SendEmailTestCase(TestCase):
    def setUp(self):
        self.email = "user@example.com"
        self.user = User.objects.create(email=self.email)
        self.user.set_password("password")
        self.user.save()

        self.request = HttpRequest()
        self.request.META["SERVER_NAME"] = "testhost"
        self.request.META["SERVER_PORT"] = 1234

    def tearDown(self):
        self.user.delete()

    def test_send_password_reset_email(self):
        send_password_reset_email(self.email, request=self.request)
        self.assertEqual(len(mail.outbox), 1)

        message = mail.outbox[0]
        self.assertEqual(message.to, [self.email])
        self.assertEqual(message.from_email, "webmaster@localhost")
        self.assertEqual(message.subject, "Password reset")
        self.assertIn(
            "http://{SERVER_NAME}:{SERVER_PORT}".format(**self.request.META),
            message.message().as_string(),
        )

    def test_send_password_reset_email_no_user(self):
        self.assertRaises(
            User.DoesNotExist,
            send_password_reset_email,
            "user.example.com",
            request=self.request,
        )

    def test_send_with_no_request(self):
        with patch("login.email.create_request_for_email") as p:
            send_password_reset_email(self.email)
            p.assert_called_once_with()
