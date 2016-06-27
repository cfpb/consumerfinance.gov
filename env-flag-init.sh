#!/bin/sh

# ==========================================================================
# Setup script for installing project dependencies.
# NOTE: Run this script while in the project root directory.
#       It will not run correctly when run from another directory.
# ==========================================================================

# Set script to exit on any errors.
set -e

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
