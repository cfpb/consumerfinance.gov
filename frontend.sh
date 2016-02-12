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
  # Set default command-line environment flag, if user didn't supply one.
  if [ -z "$1" ]; then
    cli_flag='development'
  else
    cli_flag=$1
  fi

  # Warn if unsupported command-line flag was used.
  if [ "$cli_flag" != "development" ] &&
     [ "$cli_flag" != "test" ] &&
     [ "$cli_flag" != "production" ]; then
    echo "\033[33;33mWARNING: '$cli_flag' flag not found, reverting to development environment.\033[0m"
    cli_flag='development'
  fi

  # Notify of environment that user is in.
  if [ "$cli_flag" = "development" ]; then
    echo 'Frontend:\033[33;33m development environment\033[0m.'
  elif [ "$cli_flag" = "test" ]; then
    echo 'Frontend:\033[33;1m test environment\033[0m.'
  elif [ "$cli_flag" = "production" ]; then
    echo 'Frontend:\033[32;1m production environment\033[0m.'
  fi

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
      if [ ! -d $protractor_full_path/selenium ]; then
        echo '\033[33;31mERROR: Please run `webdriver-manager update` and try again!\033[0m'
        exit
      fi
      mkdir -p ./$NODE_DIR/protractor
      cp -r $protractor_full_path ./$NODE_DIR/
    fi

  else
    npm install --production --loglevel warn
  fi
  bower install --config.interactive=false
}

# Run tasks to build the project for distribution.
build(){
  echo 'Building project...'
  gulp clean
  gulp build
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

init "$1"
clean
install
build
