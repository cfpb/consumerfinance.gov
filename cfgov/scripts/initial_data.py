from __future__ import print_function

import os

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


def run():
    print('Running script \'scripts.initial_data\' ...')

    # Create admin user if it doesn't exist already.
    User.objects.get_or_create(
        username='admin',
        defaults={
            'password': make_password(os.environ.get('WAGTAIL_ADMIN_PW')),
            'is_superuser': True,
            'is_active': True,
            'is_staff': True,
        }
    )
