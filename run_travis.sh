#!/usr/bin/env bash

# Fail if any command fails.
set -e

echo "running $RUNTEST tests"
if [ "$RUNTEST" == "frontend" ]; then
    source $HOME/.nvm/nvm.sh
    nvm use 8.0.0
    gulp "test" --travis
    gulp "test:codecov"
elif [ "$RUNTEST" == "backend" ]; then
    tox -e fast
    tox -e missing-migrations
    codecov
elif [ "$RUNTEST" == "acceptance" ]; then
    source $HOME/.nvm/nvm.sh
    nvm use 8.0.0
    export DISPLAY=:99.0
    sh -e /etc/init.d/xvfb start &
    sleep 3
    export HEADLESS_CHROME_BINARY=/usr/bin/google-chrome-beta
    gulp test:acceptance
fi
