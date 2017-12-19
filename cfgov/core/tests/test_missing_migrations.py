from cStringIO import StringIO

from django.test import TestCase

from core.scripts.missing_migrations import (
    check_missing_migrations, is_django_110_plus
)


class MissingMigrationsTestCase(TestCase):
    def test_check_for_missing_migrations(self):
        if is_django_110_plus:
            self.fail(
                'makemigrations --exit deprecated in Django 1.10: '
                'https://docs.djangoproject.com/en/1.10/ref/django-admin/'
                '#cmdoption-makemigrations--exit'
            )

        if check_missing_migrations(out=StringIO()):
            self.fail('missing migrations, run manage.py makemigrations')
