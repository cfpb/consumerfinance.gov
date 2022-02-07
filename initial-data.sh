#!/bin/bash

# ==========================================================================
# Initialization script for a wagtail user and imported data.
# NOTE: Run this script while in the project root directory.
#       It will not run correctly when run from another directory.
# ==========================================================================

# Set script to exit on any errors.
set -e

# Import Data
import_data(){
    echo 'Running Django migrations...'
    ./cfgov/manage.py migrate
    echo 'Creating any necessary Django database cache tables...'
    ./cfgov/manage.py createcachetable
    echo 'Running initial_data script to configure Wagtail admin...'
    ./cfgov/manage.py runscript initial_data
}

import_data
