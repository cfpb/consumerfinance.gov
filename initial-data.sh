#!/bin/sh

# ==========================================================================
# Initialization script for a wagtail user and imported data.
# NOTE: Run this script while in the project root directory.
#       It will not run correctly when run from another directory.
# ==========================================================================

# Set script to exit on any errors.
set -e

# Import Data
import_data(){
    echo 'Creating DB Tables...'
    ./cfgov/manage.py migrate
    echo 'Loading Initial Data...'
    ./cfgov/manage.py runscript initial_data
}

import_data
