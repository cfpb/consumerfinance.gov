from django.core.management import call_command
from django.core.management.base import SystemCheckError
from django.test import TestCase, override_settings


class SecretKeyTestCase(TestCase):
    @override_settings(SECRET_KEY="short-and-sweet", DEBUG=False)
    def test_secret_key_short(self):
        message = "(security.W009) Your SECRET_KEY has less than 50 characters"
        with self.assertRaisesMessage(SystemCheckError, message):
            call_command("check", deploy=True)

    @override_settings(
        SECRET_KEY="django-insecure-DvPKXKxsX8olubnp0QaU3XFZ3e2TZSUqr8",
        DEBUG=False,
    )
    def test_secret_key_too_django_insecure(self):
        message = "(security.W009) Your SECRET_KEY has less than 50 characters"
        with self.assertRaisesMessage(SystemCheckError, message):
            call_command("check", deploy=True)
