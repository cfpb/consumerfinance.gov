#!/usr/bin/env bash

# Install frontend dependencies
frontend() {
    npm install -g gulp-cli

    chmod +x ./frontend.sh
    ./frontend.sh development
}

# Install backend dependencies
backend() {
    pip install -r requirements/travis.txt
}

echo "installing $RUNTEST dependencies"
if [ "$RUNTEST" == "frontend" ]; then
    frontend
    backend
elif [ "$RUNTEST" == "backend" ]; then
    backend
fi
