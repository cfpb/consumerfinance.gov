from __future__ import print_function, unicode_literals

import sys

from django import VERSION
from django.core.management import call_command


try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


# Django 1.10+ includes makemigrations --check, which we can run
#  directly from tox, Travis, or the command line. So, after we
#  upgrade to Django 1.11, we will remove this file entirely.
is_django_110_plus = (1 <= VERSION[0]) and (10 <= VERSION[1])


def migrations_are_missing(out=sys.stdout):
    if is_django_110_plus:
        return migrations_missing_dj110(out)
    else:
        return migrations_missing_dj18(out)


def migrations_missing_dj18(out=sys.stdout):
    try:
        call_command(
            'makemigrations',
            exit=True,
            dry_run=True,
            stdout=out
        )
    except SystemExit:
        # No missing migrations
        return False
    else:
        # Some missing migrations
        return True


def migrations_missing_dj110(out=sys.stdout):
    try:
        call_command(
            'makemigrations',
            dry_run=True,
            check=True,
            stdout=out
        )
    except SystemExit:
        # Some missing migrations
        return True
    else:
        # No missing migrations
        return False


def run():
    out = StringIO()
    if migrations_are_missing(out):
        print("Missing migrations found:")
        print(out.getvalue())
        sys.exit(1)
    else:
        sys.exit(0)
