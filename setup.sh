#!/bin/sh

# Set script to exit on any errors.
set -e

# Initialize project dependency directories.
init(){
  NODE_DIR=node_modules
  BOWER_DIR=bower_components

  if [ -f .bowerrc ]; then
    # Get the "directory" line from .bowerrc
    BOWER_DIR=$(grep "directory" .bowerrc)
    # Strip off the first part of that line.
    BOWER_DIR=${BOWER_DIR/\"directory\"\: \"/}
    # Strip off the final " from the line.
    BOWER_DIR="${BOWER_DIR%?}"
    echo 'Bower components directory:' $BOWER_DIR
  fi
}

# Clear project dependencies.
clear(){
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
  bower install
}

# Run tasks to build the project for distribution.
build(){
  echo 'Building project...'
  grunt vendor
  grunt build
}

init
clear
install
build
