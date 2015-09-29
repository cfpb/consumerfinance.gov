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
  npm install
  bower install --config.interactive=false

  # Update test dependencies.

  # Protractor.
  ./$NODE_DIR/protractor/bin/webdriver-manager update

  # Macro Polo.
  pip install -r ./test/macro_tests/requirements.txt

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
}

init
clean
install $1
build
