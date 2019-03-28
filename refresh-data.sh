#!/bin/bash

# ==========================================================================
# Import data from a gzipped dump. Provide the filename as the first arg.
# NOTE: Run this script while in the project root directory.
#       It will not run correctly when run from another directory.
# ==========================================================================

set -e

refresh_dump_name=$1

USAGE=$(cat << 'EOF'
Please download a recent database dump before running this script:

  ./refresh-data.sh production_django.sql.gz

Or you can define the location of a dump and this script will
download it for you:

  export CFGOV_PROD_DB_LOCATION=https://example.com/production_django.sql.gz
  ./refresh-data.sh
EOF
)

download_data() {
    echo 'Downloading fresh production Django database dump...'
    prod_archive="$refresh_dump_name"
    if test -e "$prod_archive"
       then 
           curl -R -o "$prod_archive" -z "$prod_archive" "$CFGOV_PROD_DB_LOCATION"
       else
           curl -R -o "$prod_archive" "$CFGOV_PROD_DB_LOCATION"
       fi
}

refresh_data() {
    echo 'Importing refresh db'
    gunzip < "$refresh_dump_name" | cfgov/manage.py dbshell > /dev/null
    echo 'Running any necessary migrations'
    ./cfgov/manage.py migrate --noinput --fake-initial
    echo 'Setting up initial data'
    ./cfgov/manage.py runscript initial_data
}

if [[ -z "$refresh_dump_name" ]]; then
    if [[ -z "$CFGOV_PROD_DB_LOCATION" ]]; then
        printf "%s\n\n" "$USAGE"
        exit 1
    fi

    refresh_dump_name='production_django.sql.gz'
    download_data
else
    if [[ $refresh_dump_name != *.sql.gz ]]; then
        echo "Input dump '$refresh_dump_name' expected to end with .sql.gz."
        exit 2
    fi
fi

refresh_data
