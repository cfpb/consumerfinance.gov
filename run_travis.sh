#!/usr/bin/env bash

# Fail if any command fails.
set -e

echo "running $RUNTEST tests"
if [ "$RUNTEST" == "frontend" ]; then
    export CXX=clang++
    curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.31.0/install.sh | bash
    nvm install 5.5.0
    nvm use 5.5.0
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
