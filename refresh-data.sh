#!/bin/bash

# ==========================================================================
# Import data from a gzipped dump. Provide the filename as the first arg.
# NOTE: Run this script while in the project root directory.
#       It will not run correctly when run from another directory.
# ==========================================================================

set -e

usage() {
    cat << EOF
Please download a recent database dump before running this script:

  ./refresh-data.sh production_django.sql.gz

Or you can define the location of a dump and this script will
download it for you:

  export CFGOV_PROD_DB_LOCATION=https://example.com/production_django.sql.gz
  ./refresh-data.sh

Additional options:

      --noindex  Do not update search indexes after refreshing

EOF
    exit 1;
}

download_data() {
    echo 'Downloading database dump...'
    skip_download=0

    # If the file already exists, check its timestamp, and skip the download
    # if it matches the timestamp of the remote file.
    if test -e "$refresh_dump_name"; then
        timestamp_check=$(curl -s -I -R -L -z "$refresh_dump_name" "${CFGOV_PROD_DB_LOCATION:-$DB_DUMP_URL}")
        if [[ "$timestamp_check" == *"304 Not Modified"* ]]; then
            echo 'Skipping download as local timestamp matches remote timestamp'
            skip_download=1
        fi
    fi

    if [[ "$skip_download" == 0 ]]; then
        curl -RL -o "$refresh_dump_name" "${CFGOV_PROD_DB_LOCATION:-$DB_DUMP_URL}"
    fi
}

check_data() {
    echo 'Validating local dump file'
    gunzip -t "$refresh_dump_name"
}

refresh_data() {
    echo 'Importing refresh db'
    gunzip < "$refresh_dump_name" | cfgov/manage.py dbshell > /dev/null
}

initial_data() {
    ./initial-data.sh
}

update_index() {
    source ./index.sh
}

get_data() {
    if [[ -z "$refresh_dump_name" ]]; then
        if [[ -z "$CFGOV_PROD_DB_LOCATION" ]] && [[ -z "$DB_DUMP_URL" ]]; then
            usage
        fi
        if [[ ! -z "$CFGOV_PROD_DB_LOCATION" ]]; then
          refresh_dump_name='production_django.sql.gz'
        else
          # Split URL, and get the file name.
          refresh_dump_name="$(echo $DB_DUMP_URL | tr '/' '\n' | tail -1)"
        fi
        download_data
    else
        if [[ $refresh_dump_name != *.sql.gz ]]; then
            echo "Input dump '$refresh_dump_name' expected to end with .sql.gz."
            exit 2
        fi
    fi
}

noindex=false
for arg in "$@"; do
    shift
    case "$arg" in
        "--noindex")
            noindex=1
            ;;
        *)
            refresh_dump_name=$arg
            ;;
    esac
done

get_data
check_data
refresh_data
initial_data

if [[ $noindex -ne 1 ]]; then
    update_index
fi
