from django.test import TestCase

from core.scripts.missing_migrations import (
    is_django_110_plus,
    check_missing_migrations
)


class MissingMigrationsTestCase(TestCase):
    def test_check_for_missing_migrations(self):
        if is_django_110_plus:
            self.fail(
                'makemigrations --exit deprecated in Django 1.10: '
                'https://docs.djangoproject.com/en/1.10/ref/django-admin/'
                '#cmdoption-makemigrations--exit'
            )

        if check_missing_migrations():
            self.fail('missing migrations, run manage.py makemigrations')
