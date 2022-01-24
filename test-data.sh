#!/bin/bash

# ==========================================================================
# Initialization script for a Wagtail user and full set of test data.
# NOTE: This will DELETE ANY EXISTING DATA.
# NOTE: Run this script while in the project root directory.
#       It will not run correctly when run from another directory.
# ==========================================================================

# Set script to exit on any errors.
set -e

usage() {
    cat << EOF
Initialize consumerfinance.gov with an admin user and test data sufficient
for running functional tests.

WARNING: This will delete all contents of the configured Django database
and search indexes!

    -y  Do not prompt before deleting existing data.

EOF
    exit 1;
}

test_data() {
    echo 'Removing existing data...'
    ./cfgov/manage.py reset_db -c --noinput
    ./cfgov/manage.py search_index --delete -f
    echo 'Running Django migrations...'
    ./cfgov/manage.py migrate
    echo 'Creating any necessary Django database cache tables...'
    ./cfgov/manage.py createcachetable
    echo 'Running test_data script to add data required for functional testing...'
    ./cfgov/manage.py runscript test_data
}

prompt_before_deleting() {
    echo "This script will delete all existing data in the database."
    echo "Are you sure you want to do this?"
    echo
    read -p "    Type 'yes' to continue, or 'no' to cancel: "
    if [[ $REPLY =~ "yes" ]]
    then
        echo "CONTINUING"
    else
        exit 1
    fi
}

if [ $# -eq 0 ]; then
    prompt_before_deleting
else
    optstring="hy"
    while getopts ${optstring} arg; do
        case ${arg} in
            y)
                test_data
                ;;
            *)
                usage
                ;;
        esac
    done
fi
