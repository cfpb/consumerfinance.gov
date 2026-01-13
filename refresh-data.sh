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

  ./refresh-data.sh prodpub_main_django.sql.gz

Additional options:

      --noindex  Do not update search indexes after refreshing

EOF
    exit 1;
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
        refresh_dump_name='prodpub_main_django.sql.gz'
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
