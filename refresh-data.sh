#!/bin/sh

# ==========================================================================
# Import data from a dump. Provide the filename as the first arg.
# NOTE: Run this script while in the project root directory.
#       It will not run correctly when run from another directory.
# ==========================================================================

# Set script to exit on any errors.
set -e
refresh_dump_name=$1

refresh_data(){
	echo 'Dropping db'
	./drop-db.sh
	echo 'Creating db'
	./create-mysql-db.sh
	echo 'Importing refresh db'
	mysql v1 -u root -p < $refresh_dump_name
    echo 'Setting up initial data'
    ./cfgov/manage.py runscript initial_data
}

refresh_data
