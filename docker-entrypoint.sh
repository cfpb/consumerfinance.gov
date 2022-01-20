#!/bin/sh

set -e

echo "Using '$(python3 --version 2>&1)' from '$(which python3)'"

# Wait for the database to be ready
until psql ${DATABASE_URL} -c '\q' &> /dev/null; do
  >&2 echo "Postgres is unavailable - waiting"
  sleep 1
done

# Do first-time set up of the database if necessary
echo "${DATABASE_URL}"
if ! psql ${DATABASE_URL} -c 'SELECT COUNT(*) FROM auth_user' &> /dev/null; then
    echo "Doing first-time database and search index setup..."
    if [ ! -z $CFGOV_PROD_DB_LOCATION ]; then
        echo "Running refresh-data.sh..."
        ./refresh-data.sh
    else
        echo "Running initial-data.sh..."
        ./initial-data.sh
    fi
    echo "Create the cache table..."
    ./cfgov/manage.py createcachetable
    echo "Update the search indexes..."
    ./cfgov/manage.py search_index --rebuild -f --parallel
fi

# Do first-time build of the front-end if necessary
if [ ! -d "node_modules" ] && [ ! "$(ls cfgov/static_built)" ]; then
    echo "Running ./frontend.sh for the first time..."
    ./frontend.sh
fi

# Execute the Docker CMD
exec "$@"
