#!/bin/bash

# ==========================================================================
# Import data from a dump. Provide the filename as the first arg.
# NOTE: Run this script while in the project root directory.
#       It will not run correctly when run from another directory.
# ==========================================================================

# Set script to exit on any errors.
set -e
refresh_dump_name=$1

download_data() {
	echo 'Downloading fresh production Django database dump...'
	prod_archive="$refresh_dump_name".gz
	curl -o $prod_archive $CFGOV_PROD_DB_LOCATION
	gunzip -f $prod_archive
}

refresh_data(){
	echo 'Dropping db'
	./drop-db.sh
	echo 'Creating db'
	./create-mysql-db.sh
	echo 'Importing refresh db'
	mysql v1 --user='root' --password="$MYSQL_ROOT_PW" < $refresh_dump_name
	echo 'Setting up initial data'
	./cfgov/manage.py runscript initial_data
}

# If no argument was passed to the script and the db dump env variable is set
if [[ -z "$1" && ! -z "$CFGOV_PROD_DB_LOCATION" ]]; then
	refresh_dump_name='production_django.sql'
	download_data
fi

# Only attempt to load data if a db dump file is provided
if [[ -z "$refresh_dump_name" ]]; then
	echo 'Please download a recent database dump before running this script:

	./refresh-data.sh production_django.sql

Or you can define the location of a dump and this script will download it for you:

	export CFGOV_PROD_DB_LOCATION=https://example.com/wherever/production_django.sql.gz
	./refresh-data.sh
	'
else
	refresh_data
fi
