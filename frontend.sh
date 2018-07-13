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
  # Set NODE_ENV variable.
  # Set default command-line environment flag, if user didn't supply one.
  NODE_ENV=$1

  # Warn if unsupported command-line flag was used.
  if [ "$NODE_ENV" != "development" ] &&
     [ "$NODE_ENV" != "production" ]; then
    supplied_cli_flag=$NODE_ENV
    NODE_ENV='development'
    echo "WARNING: '$supplied_cli_flag' flag not found, reverting to $NODE_ENV environment."
  fi

  # Notify of environment that user is in.
  echo "Front-end environment: $NODE_ENV"

  # Set the NODE_ENV for this session.
  export NODE_ENV=$NODE_ENV
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

  if [ "$NODE_ENV" = "development" ]; then

    yarn install --ignore-engines

    # Protractor = JavaScript acceptance testing framework.
    echo "Installing Protractor dependencies locally…"
    # We skip Gecko here (--gecko false) because webdriver pulls its release
    # directly from a GitHub.com URL which enforces rate-limiting. This can
    # cause installation failures when running automated testing. Currently
    # we don't rely on Gecko for testing.
    ./node_modules/protractor/bin/webdriver-manager update --gecko false --standalone false

  else
    yarn install --production --ignore-optional
  fi
}

# Calculate checksum value.
calc_checksum() {
  DEP_CHECKSUM=$(cat yarn.lock cfgov/unprocessed/apps/**/package*.json | shasum -a 256)
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

# Analyze setup and see if we need to install dependencies.
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
  yarn run gulp build
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
