#!/bin/sh

# ==========================================================================
# Setup script for installing project dependencies.
# NOTE: Run this script while in the project root directory.
#       It will not run correctly when run from another directory.
# ==========================================================================

# Set script to exit on any errors.
set -e

# Presumes the varialble VIRTUAL_ENV is already set to the name of the venv

# Activate virtualenv, if not already activated
if ! type "$workon" &>/dev/null; then
  workon $VIRTUAL_ENV && echo "Virtualenv $VIRTUAL_ENV activated." ||
  echo 'Virtualenv was not activated.' && exit
fi
