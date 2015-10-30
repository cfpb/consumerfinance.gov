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
  NODE_DIR=node_modules
  BOWER_DIR=bower_components

  # Copy sample environment variables, if not already done.
  if [ ! -f $ENVVAR ]; then
    echo 'Setting default environment variables...'
    cp -a $ENVVAR_SAMPLE $ENVVAR
  fi

  if [ -f .bowerrc ]; then
    # Get the "directory" line from .bowerrc
    BOWER_DIR=$(grep "directory" .bowerrc | cut -d '"' -f 4)
  fi

  echo 'Environment variables:' $ENVVAR
  echo 'npm components directory:' $NODE_DIR
  echo 'Bower components directory:' $BOWER_DIR
}

# Clean project dependencies.
clean(){
  # If the node and bower directories already exist,
  # clear them so we know we're working with a clean
  # slate of the dependencies listed in package.json
  # and bower.json.
  if [ -d $NODE_DIR ] || [ -d $BOWER_DIR ]; then
    echo 'Removing project dependency directories...'
    rm -rf $NODE_DIR
    rm -rf $BOWER_DIR
  fi
  echo 'Project dependencies have been removed.'
}

# Install project dependencies.
install(){
  echo 'Installing project dependencies...'

  # Copy globally-installed packages.
  # Protractor - JavaScript acceptance testing.
  if [ $(is_installed protractor) = 0 ]; then
    echo 'Installing Protractor dependencies locally...'
    npm install protractor
    ./$NODE_DIR/protractor/bin/webdriver-manager update
  else
    echo 'Global Protractor installed. Copying global install locally...'
    protractor_symlink=$(command -v protractor)
    protractor_binary=$(readlink $protractor_symlink)
    protractor_full_path=$(dirname $protractor_symlink)/$(dirname $protractor_binary)/../../protractor
    mkdir -p ./$NODE_DIR/protractor
    cp -r $protractor_full_path ./$NODE_DIR/
  fi

  npm install
  bower install --config.interactive=false

  # Update test dependencies.

  # Macro Polo - Jinja template unit testing.
  pip install -r ./test/macro_tests/requirements.txt

  # Tox - Django server unit testing.
  pip install tox

  # Django Server
  if [ -z "$1" ]; then
    pip install -r ./requirements/base.txt
  else
    pip install -r ./requirements/$1.txt
  fi
}

# Run tasks to build the project for distribution.
build(){
  echo 'Building project...'
  gulp clean
  gulp build
  dbsetup
  gulp beep
}

# Setup MYSQL Server.
dbsetup(){
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
clean
install $1
build
