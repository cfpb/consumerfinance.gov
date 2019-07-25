#!/bin/bash --login
# NOTE: By using --login, it guarantees /etc/profile is always sourced, unlike the
# non-login, non-interactive shell you get by default with `docker run`.

set -e

echo "Using '$(python --version 2>&1)' from '$(which python)'"

# FIXME: Could we replace this with a Docker Compose env_file?
# SEE: https://docs.docker.com/compose/compose-file/#env_file
if [ -f "${APP_HOME}/.env" ]; then
    source ${APP_HOME}/.env
else
    echo "WARN: ${APP_HOME}/.env is not present."
fi

env | sort

# $INIT_DB specifies whether or not to run the initial-data.sh
if [[ ${INIT_DB} == 'ON' ]]; then
    echo 'Database init starting...'
    ${APP_HOME}/initial-data.sh
    echo 'Database init complete.'
elif [[ ${INIT_DB} == 'OFF' ]]; then
    echo 'Database init disabled.'
else
    echo "INIT_DB value '${INIT_DB}' invalid.  Must be 'ON' or 'OFF'."
    exit 1
fi

# Execute the Docker CMD
exec "$@"
