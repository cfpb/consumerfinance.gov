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

setup(){
  ./frontend.sh
  ./backend.sh $1
  gulp beep
}

init
setup $1
