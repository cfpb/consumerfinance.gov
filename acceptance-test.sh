#!/usr/bin/env bash

set -e

mysql(){
  if ! mysql.server status; then
    mysql.server start
  fi
}

npm install
gulp build
mysql
python manage.py migrate --fake-initial
lsof -i tcp:$9500| awk 'NR!=1 {print $2}' | xargs kill
python manage.py runserver 9500
