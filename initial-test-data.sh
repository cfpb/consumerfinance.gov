#!/bin/sh

# ==========================================================================
# Initialization script for a wagtail user and imported data
# NOTE: Run this script while in the project root directory.
#       It will not run correctly when run from another directory.
# ==========================================================================

# Set script to exit on any errors.
set -e

# Import Data
import_data(){
    echo 'Creating DB Tables...'
    ./cfgov/manage.py migrate --settings='cfgov.settings.test'
    echo 'Loading Initial Data...'
    ./cfgov/manage.py runscript initial_test_data --settings='cfgov.settings.test'

}

import_data
