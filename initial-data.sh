#!/bin/sh

# ==========================================================================
# Setup script for installing project dependencies.
# NOTE: Run this script while in the project root directory.
#       It will not run correctly when run from another directory.
# ==========================================================================

# Set script to exit on any errors.
set -e

# Import Data
import_data(){
    echo 'Creating DB Tables and initial data..'
    ./cfgov/manage.py migrate
    echo 'Importing Events...'
    ./cfgov/manage.py import-data contact contact --snippet -u admin -p $ADMIN_PW
    echo 'Importing Contacts...'
    ./cfgov/manage.py import-data events eventpage --parent events -u admin -p $ADMIN_PW
}

import_data
