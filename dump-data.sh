#!/bin/bash

# ==========================================================================
# Dump the contents of the $DATABASE_URL into a gzipped SQL file.
# ==========================================================================

set -e

# The filename to dump to. Defaults to test.sql.gz if empty.
dump_filename=$1
if [ -z "$dump_filename" ]; then
    dump_filename=test.sql.gz
fi

# If DATABASE_URL is not set, or is empty, default to localhost.
if [ -z "$DATABASE_URL" ]; then
    DATABASE_URL=postgres://cfpb:cfpb@localhost/cfgov
fi

dump_data() {
    # This preamble will drop the existing 'cfpb' schema if it exists.
    DROP_PREAMBLE=$(cat << EOF
SET client_min_messages = WARNING;
DROP SCHEMA IF EXISTS cfpb CASCADE;
EOF
)

    # Echo the preamble and then run pg_dump.
    # The output is piped to gzip and output to our desired output file.
    ( \
        echo "$DROP_PREAMBLE" && \
        pg_dump \
            --no-owner \
            --no-privileges \
            --user=cfpb \
            --schema=cfpb \
            $DATABASE_URL \
    ) | gzip > $dump_filename
}

dump_data
