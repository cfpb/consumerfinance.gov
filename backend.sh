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
    pip install mysql-python==1.2.4 --find-links=wheels
    pip install -r ./requirements/local.txt
  elif [ "$cli_flag" = "test" ]; then
    pip install -r ./requirements/test.txt
  elif [ "$cli_flag" = "production" ]; then
    pip install -r ./requirements/production.txt
  fi
}


# Returns 1 if a global command-line program installed, else 0.
# For example, echo "node: $(is_installed node)".
is_installed() {
  # Set to 1 initially.
  local return_=1

  # Set to 0 if program is not found.
  type $1 >/dev/null 2>&1 || { local return_=0; }

  echo "$return_"
}

init "$1"
install
sh start-services.sh
