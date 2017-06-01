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
  if [ -f "npm-shrinkwrap.json" ]; then
    DEP_CHECKSUM=$(cat npm-shrinkwrap.json package.json | shasum -a 256)
  else
    DEP_CHECKSUM=$(cat package.json | shasum -a 256)
  fi

  echo "npm components directory: $NODE_DIR"
}

# Clean project dependencies.
clean() {
  # If the node directory already exists,
  # clear it so we know we're working with a clean
  # slate of the dependencies listed in package.json.
  if [ -d $NODE_DIR ]; then
    echo 'Removing project dependency directories…'
    rm -rf $NODE_DIR
    echo 'Project dependencies have been removed.'
  fi
}

# Install project dependencies.
install() {
  echo 'Installing front-end dependencies…'

  if [ "$cli_flag" = "development" ] ||
     [ "$cli_flag" = "test" ]; then

    # Before installing dependencies,
    # create variables for globally-installed ones.
    local is_installed_protractor=$(is_installed protractor)

    npm install -d --loglevel warn

    # Copy globally-installed packages.
    # Protractor = JavaScript acceptance testing framework.
    if [ $is_installed_protractor = 0 ]; then
      echo 'Installing Protractor dependencies locally…'
      # We skip Gecko here (--gecko false) because webdriver pulls its release
      # directly from a GitHub.com URL which enforces rate-limiting. This can
      # cause installation failures when running automated testing. Currently
      # we don't rely on Gecko for testing.
      ./$NODE_DIR/protractor/bin/webdriver-manager update --gecko false
    else
      echo 'Global Protractor installed. Copying global install locally…'
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
    npm install --production --loglevel warn --no-optional
  fi
}

# Add a checksum file
checksum() {
  echo -n "$DEP_CHECKSUM" > $NODE_DIR/CHECKSUM
}

# If the node directory exists, $NODE_DIR/CHECKSUM exists, and
# the contents DO NOT match the checksum of package.json, clear
# $NODE_DIR so we know we're working with a clean slate of the
# dependencies listed in package.json.
clean_and_install() {
  if [ ! -f $NODE_DIR/CHECKSUM ] ||
     [ "$DEP_CHECKSUM" != "$(cat $NODE_DIR/CHECKSUM)" ]; then
    clean
    install
    checksum
  else
    echo 'Dependencies are up to date.'
  fi
}

# Run tasks to build the project for distribution.
build() {
  echo 'Building project…'
  gulp clean
  gulp build

  if [ "$cli_flag" = "production" ]; then
    gulp scripts:ondemand
  fi
}

shrinkwrap() {
  if [ -f "npm-shrinkwrap.json" ]; then
    echo 'Removing npm-shrinkwrap.json…'
    rm npm-shrinkwrap.json
  fi
  clean
  install
  npm prune
  echo 'Shrinkwrapping…'
  npm shrinkwrap
  checksum
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
if [ "$1" == "init" ]; then
  init ""
  clean_and_install
elif [ "$1" == "shrinkwrap" ]; then
  init "production"
  shrinkwrap
elif [ "$1" == "build" ]; then
  build
else
  init "$1"
  clean_and_install
  build
fi
