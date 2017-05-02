#!/usr/bin/env bash

set -e


lsof -i tcp:9500| awk 'NR!=1 {print $2}' | xargs kill
python manage.py runserver 9500 < /dev/null &
