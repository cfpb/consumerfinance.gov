#!/bin/sh

set -e

if [ -f '.env' ] && [ -d /var/run/secrets/kubernetes.io ]; then
  . '.env'
fi

echo "Using $(python3 --version 2>&1) located at $(which python3)"

# Do first-time set up of the database if necessary
if [ ! -z "$RUN_MIGRATIONS" ]; then
  # Wait for the database to be ready for initialization tasks
  until pg_isready --host="${PGHOST:-localhost}" --port="${PGPORT:-5432}"
  do
    echo "Waiting for postgres at: ${PGHOST:-localhost}:${PGPORT:-5432}"
    sleep 1;
  done

  # Check the DB if it needs refresh or migrations (initial-data.sh)
  if ! psql "postgres://${PGUSER:-cfpb}:${PGPASSWORD:-cfpb}@${PGHOST:-localhost}:${PGPORT:-5432}/${PGDATABASE:-cfgov}" -c 'SELECT COUNT(*) FROM auth_user' >/dev/null 2>&1 || [ ! -z $FORCE_DB_REBUILD ]; then
    echo "Doing first-time database and search index setup..."
    if [ -n "$CFGOV_PROD_DB_LOCATION" ] || [ -n "$DB_DUMP_FILE" ]; then
      echo "Running refresh-data.sh... $DB_DUMP_FILE"
      ./refresh-data.sh "$DB_DUMP_FILE"
      echo "Create the cache table..."
      ./cfgov/manage.py createcachetable

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

# Do first-time build of the front-end if necessary
if [ ! -d "node_modules" ] && [ ! "$(ls cfgov/static_built)" ]; then
    echo "Running ./frontend.sh for the first time..."
    ./frontend.sh
fi

# Execute the Docker CMD
exec "$@"
