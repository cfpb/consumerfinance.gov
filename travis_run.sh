#!/usr/bin/env bash

# Fail if any command fails.
set -ex

# Set the NODE_ENV for this script.
export NODE_ENV='development'

echo "running $RUNTEST tests"
if [ "$RUNTEST" == "frontend" ]; then
    gulp test --travis --headless
    bash <(curl -s https://codecov.io/bash) -F frontend -X coveragepy
elif [ "$RUNTEST" == "backend" ]; then
    tox -e lint
    TEST_DATABASE_URL=postgres://travis:travis@localhost:5433/travis tox -e fast
    tox -e missing-migrations
    bash <(curl -s https://codecov.io/bash) -F backend

    pip install -r requirements/manual.txt
    mkdocs build
fi
