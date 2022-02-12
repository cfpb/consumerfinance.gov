#!/bin/bash

# ==========================================================================
# Setup script for installing project dependencies.
# NOTE: Run this script while in the project root directory.
#       It will not run correctly when run from another directory.
# ==========================================================================

# Set script to exit on any errors.
set -e

init() {
  # Ensure that we're in a virtualenv.
  python -c 'import sys; sys.prefix != sys.base_prefix' 2>/dev/null || (
    echo 'Please activate your virtualenv before running this script.' &&
    exit 1
  )
}

# Install project dependencies.
install() {
  echo 'Installing back-end dependencies...'

  # Install requirements for Django Server or tox.
  pip install -r ./requirements/local.txt
}

init "$1"
install
