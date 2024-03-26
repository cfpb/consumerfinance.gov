#!/bin/sh

# ==========================================================================
# Dump the contents of the Database into a gzipped SQL file.
# ==========================================================================

set -e

# The filename to dump to. Defaults to test.sql.gz if empty.
dump_filename=$1
if [ -z "$dump_filename" ]; then
    dump_filename=test.sql.gz
fi

dump_data() {
    # This preamble will drop the existing 'cfpb' schema if it exists.
    DROP_PREAMBLE=$(cat << EOF
--
-- We add this DROP to ensure that a database dump can be loaded to generate
-- a state that exactly matches the one that was dumped. Without this, objects
-- in the schema before the dump happens may exist and conflict with the
-- dumped data being loaded.
--
SET client_min_messages = WARNING;
DROP SCHEMA IF EXISTS ${PGUSER:-cfpb} CASCADE;


EOF
)

    # Echo the preamble and then run pg_dump.
    # The output is piped to gzip and output to our desired output file.
    ( \
        echo "$DROP_PREAMBLE" && \
        pg_dump \
            --no-owner \
            --no-privileges \
            ${PGDATABASE:-cfgov}
    ) | gzip > $dump_filename
}

dump_data
