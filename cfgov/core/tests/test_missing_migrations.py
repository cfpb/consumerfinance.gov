from django import VERSION
from django.core.management import call_command
from django.test import TestCase


class MissingMigrationsTestCase(TestCase):
    def test_check_for_missing_migrations(self):
        major, minor = VERSION[0:2]
        if 1 == major and 10 <= minor:
            self.fail(
                'makemigrations --exit deprecated in Django 1.10: '
                'https://docs.djangoproject.com/en/1.10/ref/django-admin/'
                '#cmdoption-makemigrations--exit'
            )

        try:
            call_command(
                'makemigrations',
                exit=True,
                dry_run=True,
                verbosity=0
            )
        except SystemExit:
            # makemigrations calls sys.exit if there are no migrations to be
            # made. We want to detect the inverse, and fail if there are any
            # migrations that need to be generated.
            pass
        else:
            self.fail('missing migrations, run manage.py makemigrations')
