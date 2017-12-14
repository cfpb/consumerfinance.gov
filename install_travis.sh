#!/usr/bin/env bash

# Install frontend dependencies
frontend() {

    npm install -g gulp-cli

    chmod +x ./frontend.sh
    ./frontend.sh test
}

# Install backend dependencies
backend() {
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
