#!/bin/bash

# ==========================================================================
# Setup script for installing project dependencies.
# NOTE: Run this script while in the project root directory.
#       It will not run correctly when run from another directory.
# ==========================================================================

# Set script to exit on any errors.
set -e

# Confirm environment.
init() {
  # Set cli_flag variable.
  source cli-flag.sh 'Back end' $1

  # Ensure that we're in a virtualenv
  python -c 'import sys; sys.real_prefix' 2>/dev/null || (
    echo 'Please activate your virtualenv before running this script.' &&
    exit 1
  )
}


# Install project dependencies.
install() {
  echo 'Installing back-end dependencies...'

  # Install requirements for Django Server or tox.
  if [ "$cli_flag" = "development" ]; then
    pip install -r ./requirements/local.txt
  elif [ "$cli_flag" = "production" ]; then
    pip install -r ./requirements/deployment.txt
  fi
}


init "$1"
install
