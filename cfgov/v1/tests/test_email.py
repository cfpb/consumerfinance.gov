from django.contrib.auth.models import User
from django.core import mail
from django.http import HttpRequest
from django.test import TestCase

from v1.email import send_password_reset_email


class SendEmailTestCase(TestCase):
    def setUp(self):
        self.email = 'user@example.com'
        self.user = User.objects.create(email=self.email)
        self.user.set_password('password')
        self.user.save()

        self.request = HttpRequest()
        self.request.META['SERVER_NAME'] = 'testhost'
        self.request.META['SERVER_PORT'] = 1234

    def test_send_password_reset_email(self):
        send_password_reset_email(self.request, self.email)
        self.assertEqual(len(mail.outbox), 1)

        message = mail.outbox[0]
        self.assertEqual(message.to, [self.email])
        self.assertEqual(message.from_email, 'webmaster@localhost')
        self.assertEqual(message.subject, 'Password reset')
        self.assertIn(
            'http://{SERVER_NAME}:{SERVER_PORT}'.format(**self.request.META),
            message.message().as_string()
        )

    def test_send_password_reset_email_no_user(self):
        self.assertRaises(
            User.DoesNotExist,
            send_password_reset_email,
            self.request,
            'invalid_email@example.com'
        )
