#!/bin/bash --login

set -e

echo "Using '$(python --version 2>&1)' from '$(which python)'"

# Execute the Docker CMD
exec "$@"