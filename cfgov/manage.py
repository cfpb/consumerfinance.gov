#!/usr/bin/env python
import os
import sys

import dotenv


if __name__ == '__main__':
    this_dir = os.path.dirname(os.path.abspath(__file__))
    envfile_path = os.path.join(this_dir, '../.env')
    dotenv.read_dotenv(envfile_path)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cfgov.settings.local')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
