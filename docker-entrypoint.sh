#!/bin/bash --login
# NOTE: By forcing a login shell, /etc/profile is always sourced,
# unlike the non-interactive shell you get by default with `docker run`.

set -e

echo "Using '$(python --version 2>&1)' from '$(which python)'"

if [ ! -f "${APP_HOME}/.env" ]; then
    echo "ERROR: ${APP_HOME}/.env not found."
    exit 1
fi

cp ${APP_HOME}/.env /etc/profile.d/cfgov-env.sh
source /etc/profile

# Execute the Docker CMD
exec "$@"
