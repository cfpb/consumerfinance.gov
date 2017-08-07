#!/bin/bash

# ==========================================================================
# Setup script for installing project dependencies.
# NOTE: Run this script while in the project root directory.
#       It will not run correctly when run from another directory.
# ==========================================================================

# Set script to exit on any errors.
set -e

./frontend.sh $1
./backend.sh $1

if [[ ! -z "$CFGOV_SPEAK_TO_ME" ]]; then
  say "Set up has finished."
fi
