from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings

from login.email import send_password_reset_email


class SendEmailTestCase(TestCase):
    def setUp(self):
        self.email = "user@example.com"
        self.user = get_user_model().objects.create(email=self.email)
        self.user.set_password("password")
        self.user.save()

    def test_send_password_reset_email(self):
        send_password_reset_email(self.email)
        self.assertEqual(len(mail.outbox), 1)

        message = mail.outbox[0]
        self.assertEqual(message.to, [self.email])
        self.assertEqual(message.from_email, "webmaster@localhost")
        self.assertEqual(message.subject, "Password reset")
        self.assertIn(
            settings.WAGTAILADMIN_BASE_URL, message.message().as_string()
        )

    @override_settings(DEFAULT_FROM_EMAIL="from@email.com")
    def test_send_password_reset_from_email(self):
        send_password_reset_email(self.email)
        self.assertEqual(len(mail.outbox), 1)

        message = mail.outbox[0]
        self.assertEqual(message.from_email, "from@email.com")

    def test_send_password_reset_invalid_email(self):
        with self.assertRaises(ValueError):
            send_password_reset_email("this is an invalid email")
