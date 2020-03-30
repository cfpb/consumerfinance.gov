#!/usr/bin/env bash

# Fail if any command fails.
set -ex

# Set the NODE_ENV for this script.
export NODE_ENV='development'

echo "running $RUNTEST tests"
if [ "$RUNTEST" == "frontend" ]; then
    # Acceptance tests are disabled pending a webdriver update
    # yarn run gulp test --travis --headless
    yarn run gulp lint && yarn run gulp test:unit --ci --headless
    bash <(curl -s https://codecov.io/bash) -F frontend -X coveragepy
elif [ "$RUNTEST" == "backend" ]; then
    TEST_RUNNER=cfgov.test.StdoutCapturingTestRunner tox
    bash <(curl -s https://codecov.io/bash) -F backend
elif [ "$RUNTEST" == "docs" ]; then
    mkdocs build
fi
