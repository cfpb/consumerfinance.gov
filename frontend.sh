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
  source cli-flag.sh "Front-end" $1

  if [[ "$(node -v)" != "v8."* ]]; then
    echo "Please install Node 8.x: 'nvm install 8'"
    exit 1;
  fi
}

# Clean project dependencies.
clean() {
  # If the node directory already exists,
  # clear it so we know we're working with a clean
  # slate of the dependencies listed in package.json.
  if [ -d node_modules ]; then
    echo "Removing project dependency directories…"
    rm -rf node_modules
    echo "Project dependencies have been removed."
  fi
}

# Install project dependencies.
install() {
  echo "Installing front-end dependencies…"

  if [ "$cli_flag" = "development" ]; then

    npm install -d --loglevel warn

    # Protractor = JavaScript acceptance testing framework.
    echo "Installing Protractor dependencies locally…"
    # We skip Gecko here (--gecko false) because webdriver pulls its release
    # directly from a GitHub.com URL which enforces rate-limiting. This can
    # cause installation failures when running automated testing. Currently
    # we don't rely on Gecko for testing.
    ./node_modules/protractor/bin/webdriver-manager update --gecko false --standalone false

  else
    npm install --production --loglevel warn --no-optional
  fi
}

# Calculate checksum value.
calc_checksum() {
  if [ -f "package-lock.json" ]; then
    DEP_CHECKSUM=$(cat package*.json cfgov/unprocessed/apps/**/package*.json | shasum -a 256)
  else
    DEP_CHECKSUM=$(cat package.json cfgov/unprocessed/apps/**/package.json | shasum -a 256)
  fi
}

# Add a checksum file
write_checksum() {
  echo -n "$DEP_CHECKSUM" > node_modules/CHECKSUM
  echo "Wrote node_modules/CHECKSUM $DEP_CHECKSUM"
}

# Write file that says the node environment that we're in.
# We can read this on next run to see if the checksum should be bashed.
write_node_env() {
  echo -n "${NODE_ENV}" > "node_modules/NODE_ENV"
  echo "Wrote node_modules/NODE_ENV $NODE_ENV"
}

# Analyze setup and see if we need to install npm dependencies.
should_rebuild() {
  [ ! -f node_modules/NODE_ENV ] ||
  [ ! -f node_modules/CHECKSUM ] ||
  [ "$NODE_ENV" != "$(cat node_modules/NODE_ENV)" ] ||
  [ "$DEP_CHECKSUM" != "$(cat node_modules/CHECKSUM)" ]
}

# If the node directory exists, node_modules/CHECKSUM exists, and
# the contents DO NOT match the checksum of package.json, clear
# node_modules so we know we're working with a clean slate of the
# dependencies listed in package.json.
clean_and_install() {
  calc_checksum
  if should_rebuild; then
    clean
    install
    calc_checksum
    write_checksum
    write_node_env
  else
    echo "Dependencies are up to date."
  fi
}

# Run tasks to build the project for distribution.
build() {
  echo "Building project…"
  gulp build

  if [ "$cli_flag" = "production" ]; then
    echo "Running additional build steps for on-demand and Nemo assets."
    gulp scripts:ondemand
    gulp styles:ondemand
    gulp scripts:nemo
    gulp styles:nemo
  fi
}

# Execute requested (or all) functions.
if [ "$1" == "init" ]; then
  init ""
  clean_and_install
elif [ "$1" == "build" ]; then
  build
else
  init "$1"
  clean_and_install
  build
fi
