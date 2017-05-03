#!/usr/bin/env bash

set -e

python manage.py runscript initial_data
python manage.py runscript test_data


lsof -i tcp:9500| awk 'NR!=1 {print $2}' | xargs kill
python manage.py runserver 9500 < /dev/null &