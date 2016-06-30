#!/bin/sh

# ===========================================================================
# Script for setting and announcing the cli_flag variable.
# NOTE: This should only be called from frontend.sh or backend.sh.
#       The first parameter is required to be a label for which you're using.
# ===========================================================================

# Set script to exit on any errors.
set -e

# Set label for front or back end
end="$1 environment"

# Set default command-line environment flag, if user didn't supply one.
if [ -z "$2" ]; then
  cli_flag='development'
else
  cli_flag=$2
fi

# Warn if unsupported command-line flag was used.
if [ "$cli_flag" != "development" ] &&
   [ "$cli_flag" != "test" ] &&
   [ "$cli_flag" != "production" ]; then
  echo "WARNING: '$cli_flag' flag not found, reverting to development environment."
  cli_flag='development'
fi

# Notify of environment that user is in.
if [ "$cli_flag" = "development" ]; then
  echo "$end: development"
elif [ "$cli_flag" = "test" ]; then
  echo "$end: test"
elif [ "$cli_flag" = "production" ]; then
  echo "$end: production"
fi

export cli_flag=$cli_flag
