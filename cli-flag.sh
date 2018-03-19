#!/bin/bash

# ===========================================================================
# Script for setting and announcing the cli_flag variable.
# NOTE: This should only be called from frontend.sh or backend.sh.
#       The first parameter is required to be a label for which you're using.
# ===========================================================================

# Set script to exit on any errors.
set -e

if [ -z "$1" ]; then
  echo "ERROR: cli-flag.sh should only be called from frontend.sh or backend.sh."
  exit
fi

# Set default command-line environment flag, if user didn't supply one.
cli_flag=$2

# Warn if unsupported command-line flag was used.
if [ "$cli_flag" != "development" ] &&
   [ "$cli_flag" != "production" ]; then
  supplied_cli_flag=$cli_flag
  cli_flag='development'
  echo "WARNING: '$supplied_cli_flag' flag not found, reverting to $cli_flag environment."
fi

# Set label for front or back end
end="$1 environment"

# Notify of environment that user is in.
echo "$end: $cli_flag"

export cli_flag=$cli_flag
