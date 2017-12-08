#!/bin/bash

# ==========================================================================
# Setup script for running Django Server
# NOTE: Run this script while in the project root directory.
#       It will not run correctly when run from another directory.
# ==========================================================================

# Set script to exit on any errors.
set -e

standalone() {
    mysql(){
    if ! mysql.server status; then
        mysql.server start
    fi
    }

    # Run tasks to build the project for distribution.
    server(){
    if [ "$1" == "ssl" ]; then
        echo '\033[0;32mStarting SSL Django server on port' $DJANGO_HTTP_PORT '...'
        python cfgov/manage.py runsslserver $DJANGO_HTT_PORT
    else
        echo '\033[0;32mStarting the Django server on port' $DJANGO_HTTP_PORT '...'
        python cfgov/manage.py runserver $DJANGO_HTTP_PORT
    fi
    }

    mysql
    server "$1"
}

dockerized() {
    source mac-virtualbox-init.sh
    docker-compose up
}

check_if_docker_installed() {
    if [ -x "$(command -v docker)" ]; then
        echo "Docker is installed."
    else
        echo "Docker not installed. See installation.md for installing docker."
    fi
}

# Execute requested (or all) functions.
if [ "$1" == "docker" ]; then
    check_if_docker_installed
    dockerized
else
    standalone
fi
