#!/bin/sh

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
  if [ "$NODE_ENV" = "development" ]; then
    echo "Installing frontend development dependencies…"
    yarn install
  else
    echo "Installing frontend production dependencies…"
    yarn install --production
  fi
}

# Run tasks to build the project for distribution.
build() {
  echo "Building project…"
  yarn build
}

# Execute requested (or all) functions.
if [ "$1" = "init" ]; then
  init ""
  install
elif [ "$1" = "build" ]; then
  build
else
  init "$1"
  install
  build
fi
