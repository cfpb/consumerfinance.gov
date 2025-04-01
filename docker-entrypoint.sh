#!/bin/sh

set -e

if [ -f '.env' ]; then
  . '.env'
fi

echo "Using $(python3 --version 2>&1) located at $(which python3)"

# Do first-time set up of the database if necessary
if [ ! -z "$RUN_MIGRATIONS" ]; then
  # Wait for the database to be ready for initialization tasks
  until psql "$DATABASE_URL" -c '\q' >/dev/null 2>&1
  do
    echo "Waiting for postgres at $DATABASE_URL"
    sleep 1;
  done

  # Check the DB if it needs refresh or migrations (initial-data.sh)
  if ! psql "$DATABASE_URL" -c 'SELECT COUNT(*) FROM auth_user' >/dev/null 2>&1 || [ ! -z $FORCE_DB_REBUILD ]; then
    echo "Doing first-time database and search index setup..."
    if [ -n "$CFGOV_PROD_DB_LOCATION" ] || [ -n "$DB_DUMP_FILE" ] || [ -n "$DB_DUMP_URL" ]; then
      echo "Running refresh-data.sh... $DB_DUMP_FILE"
      ./refresh-data.sh "$DB_DUMP_FILE"

      # refresh-data.sh runs migrations and rebuilds index,
      # unset vars to prevent further action
      unset RUN_MIGRATIONS
      unset REBUILD_INDEX
    else
      # Detected the database is empty, or force rebuild was requested,
      # but we have no valid data sources to load data.
      echo "WARNING: Database rebuild request detected, but missing CFGOV_PROD_DB_LOCATION/DB_DUMP_FILE variable (one or the other is needed). Unable to load data!!"
    fi
  else
    echo "Data detected, FORCE_DB_REBUILD not requested. Skipping data load!"
  fi

  # Check if we still need to run migrations, if so, run them
  if [ ! -z $RUN_MIGRATIONS ]; then
    echo "Running initial-data.sh (migrations)..."
    ./initial-data.sh
  fi
fi

# Check if we need to rebuild index
if [ ! -z $REBUILD_INDEX ]; then
  echo "Rebuilding Search Indexes..."
  django-admin opensearch index --force rebuild
  django-admin opensearch document --force --refresh index
fi

# Execute the Docker CMD
exec "$@"
