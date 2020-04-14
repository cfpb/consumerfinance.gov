#!/usr/bin/env bash

# Install frontend dependencies
frontend() {
    npm install --global gulp-cli
    chmod +x ./frontend.sh
    ./frontend.sh development
}

# Install backend dependencies
backend() {
    pip install -r requirements/ci.txt
}

docs() {
    pip install -r requirements/docs.txt
}

echo "Installing $RUNTEST dependencies"
if [ "$RUNTEST" == "frontend" ]; then
    frontend
    backend
elif [ "$RUNTEST" == "backend" ]; then
    backend
elif [ "$RUNTEST" == "docs" ]; then
    docs
fi
