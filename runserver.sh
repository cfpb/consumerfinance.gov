#!/bin/bash

# ==========================================================================
# Setup script for running Django Server
# NOTE: Run this script while in the project root directory.
#       It will not run correctly when run from another directory.
# ==========================================================================

# Set script to exit on any errors.
set -e

DJANGO_HTTP_PORT=${DJANGO_HTTP_PORT:-8000}

if [ "$1" == "ssl" ]; then
  echo -e '\033[0;32mStarting SSL Django server on port' $DJANGO_HTTP_PORT '...'
  tput sgr0
  python cfgov/manage.py runsslserver $DJANGO_HTTP_PORT
else
  echo -e '\033[0;32mStarting the Django server on port' $DJANGO_HTTP_PORT '...'
  tput sgr0
  python cfgov/manage.py runserver $DJANGO_HTTP_PORT
fi
