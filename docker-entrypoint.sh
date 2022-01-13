#!/bin/bash --login

set -e

echo "Using '$(python3 --version 2>&1)' from '$(which python3)'"

# Execute the Docker CMD
exec "$@"