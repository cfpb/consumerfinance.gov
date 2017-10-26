#!/bin/sh

# ==========================================================================
# Setup script for running Django Server
# NOTE: Run this script while in the project root directory.
#       It will not run correctly when run from another directory.
# ==========================================================================

# Set script to exit on any errors.
set -e

mysql(){
  if ! mysql.server status; then
    mysql.server start
  fi
}

# Run tasks to build the project for distribution.
server(){
  if [ "$1" == "ssl" ]; then
    echo '\033[0;32mStarting SSL Django server on port' $DJANGO_HTTP_PORT '...'
    python cfgov/manage.py runsslserver $DJANGO_HTT_PORT
  else
    echo '\033[0;32mStarting the Django server on port' $DJANGO_HTTP_PORT '...'
    python cfgov/manage.py runserver $DJANGO_HTTP_PORT
  fi
}

mysql
server "$1"


