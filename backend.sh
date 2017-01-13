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
  elif [ "$cli_flag" = "test" ]; then
    pip install -r ./requirements/test.txt
  elif [ "$cli_flag" = "production" ]; then
    pip install -r ./requirements/base.txt
  fi
}

# Setup MySQL server.
db_setup() {
  echo 'Setting up MySQL database...'
  if [ $(is_installed mysql.server) = 1 ]; then
    if mysql.server status; then
      ./create-mysql-db.sh
    else
      mysql.server start
      ./create-mysql-db.sh
    fi

    if [ "$cli_flag" = "development" ]; then
      ./initial-data.sh
    fi
  else
    echo 'Error: MySQL not found. Please install MySQL.'
    echo 'The easiest way to do this is probably by running'
    echo '$ brew install mysql'
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
db_setup
