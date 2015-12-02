#!/bin/sh

# ==========================================================================
# Setup script for installing project dependencies.
# NOTE: Run this script while in the project root directory.
#       It will not run correctly when run from another directory.
# ==========================================================================

# Set script to exit on any errors.
set -e

# Initialize project dependency directories.
init(){
  ENVVAR_SAMPLE=.env_SAMPLE
  ENVVAR=.env

  # Copy sample environment variables, if not already done.
  if [ ! -f $ENVVAR ]; then
    echo 'Setting default environment variables...'
    cp -a $ENVVAR_SAMPLE $ENVVAR
  fi

  echo 'Environment variables:' $ENVVAR
}


# Build project dependencies.
build(){
  echo 'Installing project dependencies...'

  # Update test dependencies.
  # Macro Polo - Jinja template unit testing.
  pip install -r ./test/macro_tests/requirements.txt

  # Tox - Django server unit testing.
  pip install tox

  # Django Server
  if [ -z "$1" ]; then
    pip install -r ./requirements/local.txt
  else
    pip install -r ./requirements/$1.txt
  fi

  dbsetup
}

# Setup MYSQL Server.
dbsetup(){
  echo 'Setting Up Mysql DB'
  if [ $(is_installed mysql.server) = 1 ]; then
    if mysql.server status; then
      ./create-mysql-db.sh
    else
      mysql.server start
      ./create-mysql-db.sh
    fi
  else
    echo 'Please install MYSQL Server.'
    exit
  fi
}

# Returns 1 if a global command-line program installed, else 0.
# For example, echo "node: $(is_installed node)".
is_installed(){
  # Set to 1 initially.
  local return_=1

  # Set to 0 if program is not found.
  type $1 >/dev/null 2>&1 || { local return_=0; }

  echo "$return_"
}

init
build $1

