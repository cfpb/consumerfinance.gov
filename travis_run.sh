#!/usr/bin/env bash

# Fail if any command fails.
set -ex

echo "running $RUNTEST tests"
if [ "$RUNTEST" == "frontend" ]; then
    gulp test --travis
    bash <(curl -s https://codecov.io/bash) -F frontend
elif [ "$RUNTEST" == "backend" ]; then
    tox -e lint
    DATABASE_URL=postgres://postgres@localhost/travis_ci_test tox -e fast
    tox -e missing-migrations
    bash <(curl -s https://codecov.io/bash) -F backend
elif [ "$RUNTEST" == "acceptance" ]; then
    gulp test:acceptance --headless
fi
