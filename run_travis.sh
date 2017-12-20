#!/usr/bin/env bash

# Fail if any command fails.
set -x

echo "running $RUNTEST tests"
if [ "$RUNTEST" == "frontend" ]; then
    source $HOME/.nvm/nvm.sh
    gulp "test" --travis
    bash <(curl -s https://codecov.io/bash) -F frontend
elif [ "$RUNTEST" == "backend" ]; then
    flake8
    isort --check-only --diff --recursive cfgov
    tox -e fast
    tox -e missing-migrations
    bash <(curl -s https://codecov.io/bash) -F backend
elif [ "$RUNTEST" == "acceptance" ]; then
    source $HOME/.nvm/nvm.sh
    export DISPLAY=:99.0
    sleep 3
    gulp test:acceptance
fi
