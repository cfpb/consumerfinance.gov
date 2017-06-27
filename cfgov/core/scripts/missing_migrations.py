from __future__ import unicode_literals, print_function

import sys

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from django import VERSION
from django.core.management import call_command


def run():
    major, minor = VERSION[0:2]
    if 1 == major and 10 <= minor:
        print(
            'makemigrations --exit deprecated in Django 1.10: '
            'https://docs.djangoproject.com/en/1.10/ref/django-admin/'
            '#cmdoption-makemigrations--exit'
        )
        sys.exit(1)

    out = StringIO()
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
        pass
    else:
        print("Missing migrations found:")
        print(out.getvalue())
        sys.exit(1)
