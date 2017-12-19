from __future__ import print_function, unicode_literals

import sys

from django import VERSION
from django.core.management import call_command


try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


# Django 1.10+ includes makemigrations --check, making this unnecessary
is_django_110_plus = (1 <= VERSION[0]) and (10 <= VERSION[1])


def check_missing_migrations(out=sys.stdout):
    try:
        call_command(
            'makemigrations',
            exit=True,
            dry_run=True,
            stdout=out
        )
    except SystemExit:
        # makemigrations calls sys.exit if there are no migrations to be
        # made. We want to detect the inverse, and fail if there are any
        # migrations that need to be generated.
        return False
    else:
        return True


def run():
    if is_django_110_plus:
        print(
            'makemigrations --exit deprecated in Django 1.10: '
            'https://docs.djangoproject.com/en/1.10/ref/django-admin/'
            '#cmdoption-makemigrations--exit'
        )

    out = StringIO()
    if check_missing_migrations(out):
        print("Missing migrations found:")
        print(out.getvalue())
        sys.exit(1)
