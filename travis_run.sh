#!/usr/bin/env bash

# Fail if any command fails.
set -ex

echo "running $RUNTEST tests"
if [ "$RUNTEST" == "frontend" ]; then
    gulp test --travis
    bash <(curl -s https://codecov.io/bash) -F frontend
elif [ "$RUNTEST" == "backend" ]; then
    tox -e lint
    tox -e fast
    tox -e missing-migrations
    bash <(curl -s https://codecov.io/bash) -F backend
elif [ "$RUNTEST" == "acceptance" ]; then
    export DISPLAY=:99.0
    sh -e /etc/init.d/xvfb start &
    sleep 3
    gulp test:acceptance
fi
