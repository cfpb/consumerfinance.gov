#!/usr/bin/env bash

# Fail if any command fails.
set -e

echo "running $RUNTEST tests"
if [ "$RUNTEST" == "frontend" ]; then
    gulp "test:unit"
    gulp "test:coveralls"
elif [ "$RUNTEST" == "backend" ]; then
    # Run flake8 first for more efficient Travis failures.
    flake8

    # Run tox in "fast" mode (skipping most Django migrations).
    tox -e fast

    # Report code coverage to coveralls.io.
    coveralls
elif [ "$RUNTEST" == "acceptance" ]; then
    export DISPLAY=:99.0
    sh -e /etc/init.d/xvfb start &
    sleep 3
    export HEADLESS_CHROME_BINARY=/usr/bin/google-chrome-beta
    gulp test:acceptance
fi
