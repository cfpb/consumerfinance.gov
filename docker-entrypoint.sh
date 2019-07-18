#!/bin/bash

set -ex

source ${APP_HOME}/.env

env | sort

if [[ ${INIT_DB} == 'ON' ]]; then
    echo 'Database init starting...'
    ${APP_HOME}/initial-data.sh
    echo 'Database init complete'
elif [[ ${INIT_DB} == 'OFF' ]]; then
    echo 'Database init disabled'
else
    echo "INIT_DB value ${INIT_DB} invalid.  Must be 'ON' or 'OFF'"
    exit 1
fi

${APP_HOME}/cfgov/manage.py runserver 0.0.0.0:8000
