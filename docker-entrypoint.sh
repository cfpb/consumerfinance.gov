#!/bin/bash --login

set -e

# Add .env to to /etc/profile
if [ ! -f "${APP_HOME}/.env" ]; then
    echo "WARNING: ${APP_HOME}/.env not found."
else
    cp ${APP_HOME}/.env /etc/profile.d/cfgov-env.sh
fi

# source all the env scripts added to /etc/profile.d/ at build and runtime
source /etc/profile

echo "Using '$(python --version 2>&1)' from '$(which python)'"

# Execute the Docker CMD
exec "$@"