#!/usr/bin/env bash

# Install frontend dependencies
frontend() {
    export CXX=clang++

    # Temporarily commented out to deal with default Node version issues
    #if [[ "$(node -v)" != 'v6.'* ]]; then
    #    curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.2/install.sh | bash
    #    source ~/.nvm/nvm.sh
    #    nvm install 6
    #fi

    npm install -g gulp npm@3.10.10
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
