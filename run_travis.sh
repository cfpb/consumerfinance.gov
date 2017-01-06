#!/usr/bin/env bash

# Fail if any command fails.
set -e

echo "running $RUNTEST tests"
if [ "$RUNTEST" == "frontend" ]; then
    npm install -g gulp
    chmod +x ./frontend.sh
    # ./frontend.sh test
    gulp "test:unit"
    gulp "test:coveralls"
elif [ "$RUNTEST" == "backend" ]; then
    pip install -r requirements/travis.txt
    tox -e travis
    coveralls
fi
