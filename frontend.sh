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
    yarn install --production --ignore-optional
  fi
}

# Run tasks to build the project for distribution.
build() {
  echo "Building project…"
  yarn run gulp build
}

# Fake our font files, if necessary, in public CI
fake_fonts() {
  if [ ! -d static.in/cfgov-fonts/fonts ]; then
    echo "Faking font files…"
    # We want to test Django collectstatic, but we might not have our webfont
    # files if this script is running somewhere public. Because consumerfinance.gov
    # uses the Django ManifestStaticFilesStorage backend, the collectstatic
    # command will fail if any referenced files are missing.
    #
    # Builds generated with webfont files place them in a static.in/0/fonts
    # subdirectory. Builds generated without these files don't have this
    # directory.
    #
    # If we don't have the webfont files, we create empty files with the same
    # name to allow collectstatic to run successfully. If the files already
    # exist, these commands do nothing.
    mkdir -p static.in/fake-fonts/fonts

    # 1. Use grep to find all .woff and .woff2 files referenced in CSS files.
    # 2. Reduce these to a list of unique webfont filenames.
    # 3. Touch each filename in static.in/fake-fonts/fonts, causing it to be created as
    # an empty file if it doesn't exist already.
    grep -Eho \
        '[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}.woff2?' \
        cfgov/static_built/css/*.css \
        | sort \
        | uniq \
        | sed 's|^|static.in/fake-fonts/fonts/|' \
        | xargs touch
  fi
}

# Execute requested (or all) functions.
if [ "$1" = "init" ]; then
  init ""
  install
elif [ "$1" = "build" ]; then
  build
elif [ "$1" = "ci" ]; then
  init "production"
  install
  build
  fake_fonts
else
  init "$1"
  install
  build
fi
