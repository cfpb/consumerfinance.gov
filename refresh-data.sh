#!/bin/bash

# ==========================================================================
# Import data from a gzipped dump. Provide the filename as the first arg.
# NOTE: Run this script while in the project root directory.
#       It will not run correctly when run from another directory.
# ==========================================================================

# Set script to exit on any errors.
set -e
refresh_dump_name=$1

download_data() {
	echo 'Downloading fresh production Django database dump...'
	prod_archive="$refresh_dump_name"
	curl -o "$prod_archive" "$CFGOV_PROD_DB_LOCATION"
}

refresh_data(){
	echo 'Importing refresh db'
	gunzip < "$refresh_dump_name" | cfgov/manage.py dbshell
	echo 'Running any necessary migrations'
	./cfgov/manage.py migrate --noinput
	echo 'Setting up initial data'
	./cfgov/manage.py runscript initial_data
}

# If dump name wasn't provided.
if [[ -z "$refresh_dump_name" ]]; then
    # If URL to download from wasn't provided.
    if [[ -z "$CFGOV_PROD_DB_LOCATION" ]]; then
	    echo 'Please download a recent database dump before running this script:

	./refresh-data.sh production_django.sql

Or you can define the location of a dump and this script will download it for you:

	export CFGOV_PROD_DB_LOCATION=https://example.com/wherever/production_django.sql.gz
	./refresh-data.sh
'
        exit 1;
    fi

    # URL was provided, so set dump name and download it.
    refresh_dump_name='production_django.sql.gz'
    download_data
else
    # Dump name was provided. Verify that it's in the expected format.
    if [[ $refresh_dump_name != *.sql.gz ]]; then
        echo "Input dump '$refresh_dump_name' expected to end with .sql.gz."
        exit 2;
    fi
fi

# We have a dump and it should be the right format. Load it.
refresh_data
