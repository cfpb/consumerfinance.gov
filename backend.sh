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
  # Set default command-line environment flag, if user didn't supply one.
  if [ -z "$1" ]; then
    cli_flag='development'
  else
    cli_flag=$1
  fi

  # Warn if unsupported command-line flag was used.
  if [ "$cli_flag" != "development" ] &&
     [ "$cli_flag" != "test" ] &&
     [ "$cli_flag" != "production" ]; then
    echo "\033[33;33mWARNING: '$cli_flag' flag not found, reverting to development environment.\033[0m"
    cli_flag='development'
  fi

  # Notify of environment that user is in.
  if [ "$cli_flag" = "development" ]; then
    echo 'Frontend:\033[33;33m development environment\033[0m.'
  elif [ "$cli_flag" = "test" ]; then
    echo 'Frontend:\033[33;1m test environment\033[0m.'
  elif [ "$cli_flag" = "production" ]; then
    echo 'Frontend:\033[32;1m production environment\033[0m.'
  fi

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

  # Install requirements for Django Server or tox.
  if [ "$cli_flag" = "development" ]; then
    pip install -r ./requirements/local.txt
  elif [ "$cli_flag" = "test" ]; then
    pip install -r ./requirements/test.txt
  elif [ "$cli_flag" = "production" ]; then
    pip install -r ./requirements/base.txt
  fi

  # Update test dependencies.
  # Macro Polo - Jinja template unit testing.
  pip install -r ./test/macro_tests/requirements.txt

  # Tox - Django server unit testing.
  pip install tox

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

init "$1"
build
