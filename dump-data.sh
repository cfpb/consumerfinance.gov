#!/bin/bash

# ==========================================================================
# Dump the contents of the database into a gzipped SQL file.
#
# Optionally provide the name of the file to create:
#
# ./dump-data.sh <dump.sql.gz>
#
# Database URL must be specified with the DATABASE_URL environment variable.
# See https://github.com/jazzband/dj-database-url for URL formatting.
# ==========================================================================

set -e

# Ensure that the DATABASE_URL environment variable is set.
: "${DATABASE_URL?The DATABASE_URL environment variable must be set.}"

# Dump filename defaults to test.sql.gz if not provided on the command line.
dump_filename=$1
dump_filename=${dump_filename:-test.sql.gz}

# Pipe the output of pg_dump to gzip and then to our desired output file.
pg_dump \
    --no-owner \
    --no-privileges \
    --clean \
    --if-exists \
    $DATABASE_URL \
| gzip > $dump_filename
