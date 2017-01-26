#!/bin/bash

# ==========================================================================
# Setup script for installing project dependencies.
# NOTE: Run this script while in the project root directory.
#       It will not run correctly when run from another directory.
# ==========================================================================

# Set script to exit on any errors.
set -e

# Initialize project dependency directories.
init() {
  # Set cli_flag variable.
  source cli-flag.sh 'Front end' $1

  NODE_DIR=node_modules
  DEP_CHECKSUM=`cat npm-shrinkwrap.json package.json | shasum -a 256`

  echo "npm components directory: $NODE_DIR"
}

# Clean project dependencies if needed
clean() {
  # If the node directory exists, $NODE_DIR/CHECKSUM exists, and
  # the contents DO NOT match the checksum of package.json, clear
  # $NODE_DIR so we know we're working with a clean slate of the
  # dependencies listed in package.json.
  if [ -d $NODE_DIR ]; then
    echo $DEP_CHECKSUM
    echo `cat $NODE_DIR/CHECKSUM`
    if [ ! -f $NODE_DIR/CHECKSUM ] || 
       [ "$DEP_CHECKSUM" != "`cat $NODE_DIR/CHECKSUM`" ]; then
      echo 'Removing project dependency directories...'
      rm -rf $NODE_DIR
      echo 'Project dependencies have been removed.'
    else
      echo 'Project dependencies checksum matches package.json...'
    fi
  fi
}

# Install project dependencies.
install() {
  echo 'Installing front-end dependencies...'

  if [ "$cli_flag" = "development" ] ||
     [ "$cli_flag" = "test" ]; then

    # Before installing dependencies,
    # create variables for globally-installed ones.
    local is_installed_protractor=$(is_installed protractor)

    npm install -d --loglevel warn

    # Copy globally-installed packages.
    # Protractor = JavaScript acceptance testing framework.
    if [ $is_installed_protractor = 0 ]; then
      echo 'Installing Protractor dependencies locally...'
      ./$NODE_DIR/protractor/bin/webdriver-manager update
    else
      echo 'Global Protractor installed. Copying global install locally...'
      protractor_symlink=$(command -v protractor)
      protractor_binary=$(readlink $protractor_symlink)
      protractor_full_path=$(dirname $protractor_symlink)/$(dirname $protractor_binary)/../../protractor
      if [ ! -d $protractor_full_path/node_modules/webdriver-manager/selenium ]; then
        echo 'ERROR: Please run `webdriver-manager update` and try again!'
        exit
      fi
      mkdir -p ./$NODE_DIR/protractor
      cp -r $protractor_full_path ./$NODE_DIR/
    fi

  else
    npm install --production --loglevel warn
  fi

  # Add a checksum file
  if  [ ! -f $NODE_DIR/CHECKSUM ]; then
    echo -n $DEP_CHECKSUM > $NODE_DIR/CHECKSUM
  fi
}

# Run tasks to build the project for distribution.
build() {
  echo 'Building project...'
  gulp clean
  gulp build

  if [ "$cli_flag" = "production" ]; then
    gulp scripts:ondemand
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

# Execute requested (or all) functions.
if [ "$1" == "init" ] || [ "$1" == "build" ]; then
  if [ "$1" == "init" ]; then
    init ""
    clean
    install
  else
    build
  fi
else
  init "$1"
  clean
  install
  build
fi
