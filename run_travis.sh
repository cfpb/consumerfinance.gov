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
elif [ "$RUNTEST" == "acceptance" ]; then
    export DISPLAY=:99.0
    sh -e /etc/init.d/xvfb start &
    sleep 3

    gulp test:acceptance
fi
