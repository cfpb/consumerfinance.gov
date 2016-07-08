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
	mysql v1 -u root -p -e 'drop database v1;'
	echo 'Creating db'
	./create-mysql-db.sh
	echo 'Importing refresh db'
	mysql v1 -u root -p < $refresh_dump_name
    echo 'Running migrations'
    ./cfgov/manage.py migrate --fake
    echo 'Setting up Sites'
    ./cfgov/manage.py runscript setup_sites
}

refresh_data

