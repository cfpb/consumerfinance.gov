#!/usr/bin/env bash

# Install frontend dependencies
frontend() {
    export CXX=clang++

    if [[ "$(node -v)" != 'v6.'* ]]; then
        curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.2/install.sh | bash
        source ~/.nvm/nvm.sh
        nvm install 6
    fi

    node_modules="-g gulp"
    npm_version="3.10.7"

    if [[ "$(npm -v)" != "$npm_version" ]]; then
        node_modules="$node_modules npm@$npm_version"
    fi

    npm install "$node_modules"
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
