#!/bin/sh

# ==========================================================================
# Setup script for running Django Server
# NOTE: Run this script while in the project root directory.
#       It will not run correctly when run from another directory.
# ==========================================================================

# Set script to exit on any errors.
set -e

# Run tasks to build the project for distribution.
run(){
  echo 'Running Server...'
  python cfgov/manage.py collectstatic --clear --noinput
  touch cfgov/static/.gitkeep
  python cfgov/manage.py runserver
}

run
