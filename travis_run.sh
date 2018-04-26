#!/usr/bin/env bash

# Fail if any command fails.
set -ex

echo "running $RUNTEST tests"
if [ "$RUNTEST" == "frontend" ]; then
    gulp test --travis --headless
    bash <(curl -s https://codecov.io/bash) -F frontend -X coveragepy
elif [ "$RUNTEST" == "backend" ]; then
    tox -e lint
    DATABASE_URL=postgres://postgres@localhost/travis_ci_test tox -e fast
    tox -e missing-migrations
    bash <(curl -s https://codecov.io/bash) -F backend

    pip install -r requirements/manual.txt
    mkdocs build
fi
