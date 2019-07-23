#!/usr/bin/env python
import os
import sys

import dotenv

this_dir = os.path.dirname(os.path.abspath(__file__))


def initialize_environment():
    environment_candidates = [
        os.path.join(this_dir, '.env'),
        os.path.join(this_dir, '../.env'),
        os.path.join(os.getcwd(), '.env')
    ]

    for candidate in environment_candidates:
        if os.path.exists(candidate):
                dotenv.read_dotenv(candidate)
                return


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cfgov.settings.local')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
