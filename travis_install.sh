#!/usr/bin/env bash

# Install frontend dependencies
frontend() {
    npm install -g gulp-cli

    chmod +x ./frontend.sh
    ./frontend.sh development
}

# Install backend dependencies
backend() {
    npm install -g gulp-cli
    npm install cf-icons
    gulp copy:icons
    pip install -r requirements/travis.txt
}

echo "installing $RUNTEST dependencies"
if [ "$RUNTEST" == "frontend" ]; then
    frontend
elif [ "$RUNTEST" == "backend" ]; then
    backend
elif [ "$RUNTEST" == "acceptance" ]; then
    frontend
    backend
fi
