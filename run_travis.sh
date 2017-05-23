#!/usr/bin/env bash

# Fail if any command fails.
set -e

echo "running $RUNTEST tests"
if [ "$RUNTEST" == "frontend" ]; then
    gulp "test:unit"
    gulp "test:coveralls"
elif [ "$RUNTEST" == "backend" ]; then
    tox
    flake8
    coveralls
fi
