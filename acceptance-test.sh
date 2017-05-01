#!/bin/bash

set -e

npm install
gulp build
killall -9 mysqld mysqld_safe
mysql.server start
python manage.py migrate --fake-initial
lsof -i tcp:$9500| awk 'NR!=1 {print $2}' | xargs kill
python manage.py runserver 9500
