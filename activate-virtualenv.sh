#!/bin/sh

# ==========================================================================
# Script for activating the virtualenv (creating it first, if necessary).
# NOTE: Run this script while in the project root directory.
#       It will not run correctly when run from another directory.
# ==========================================================================

# Set script to exit on any errors.
set -e

# Presumes the varialble VIRTUAL_ENV is already set to the name of the venv

echo 'Activating virtualenv, if not already activated...'

source $(brew --prefix)/bin/virtualenvwrapper.sh

# Activate virtualenv, if not already activated
if ! type "$workon" &>/dev/null; then
  if workon $VENV_NAME; then
    echo "Virtualenv $VENV_NAME activated."
  else
    echo "Attempting to create new virtualenv $VENV_NAME..."
    if mkvirtualenv $VENV_NAME; then
      echo "Virtualenv $VENV_NAME created and activated."
    else
      echo 'Error: virtualenv not activated.' \
           'Are virtualenv and virtualenvwrapper installed?'
    fi
  fi
fi
