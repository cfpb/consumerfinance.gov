#!/bin/sh

# ==========================================================================
# Setup script for running Django Server
# NOTE: Run this script while in the project root directory.
#       It will not run correctly when run from another directory.
# ==========================================================================

# Set script to exit on any errors.
set -e

# make sure backend services are running
source start-services.sh

if [ -z "$DJANGO_HTTP_PORT"]; then
  DJANGO_HTTP_PORT=8000
fi

server(){
  if [ "$1" == "ssl" ]; then
    echo '\033[0;32mStarting SSL Django server on port' $DJANGO_HTTP_PORT '...'
    python cfgov/manage.py runsslserver $DJANGO_HTT_PORT
  else
    echo '\033[0;32mStarting the Django server on port' $DJANGO_HTTP_PORT '...'
    python cfgov/manage.py runserver $DJANGO_HTTP_PORT
  fi
}

server "$1"

