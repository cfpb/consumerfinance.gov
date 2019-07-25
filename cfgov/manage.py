#!/usr/bin/env python
import json
import os
import sys

import dotenv


if __name__ == '__main__':
    this_dir = os.path.dirname(os.path.abspath(__file__))
    envfile_path = os.path.join(this_dir, '../.env')
    environmentdotjson_path = os.path.join(this_dir, '../environment.json')
    if os.path.exists(envfile_path):
        dotenv.read_dotenv(envfile_path, override=True)

    elif os.path.exists(environmentdotjson_path):
        with open(environmentdotjson_path) as environmentdotjson:
            new_env_vars = json.load(environmentdotjson)
            os.environ.update(new_env_vars)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cfgov.settings.local')

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
