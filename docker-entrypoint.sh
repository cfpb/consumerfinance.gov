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

# Execute the Docker CMD
exec "$@"
