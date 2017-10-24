#!/usr/bin/env bash

if [ -z $RUNTEST ]; then
    RUNTEST=$1
fi


# Install frontend dependencies
frontend() {
    export CXX=clang++

    if [[ "$(node -v)" != 'v8.'* ]]; then
        curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.2/install.sh | bash
        source $HOME/.nvm/nvm.sh
        nvm install 8.0.0
    fi

    npm install -g gulp-cli

    # Added to fix an issue with gulp not being accessible in run_travis.sh
    echo 'PATH=/home/travis/.nvm/versions/node/v8.0.0/lib/node_modules/gulp-cli/bin/gulp.js:$PATH' >> ~/.bash_profile

    chmod +x ./frontend.sh
    ./frontend.sh test
}

# Install backend dependencies
backend() {
    pip install -r requirements/travis.txt
}

# Fail if any command fails.
set -e

echo "running $RUNTEST tests"
if [ "$RUNTEST" == "frontend" ]; then
    frontend
    source $HOME/.nvm/nvm.sh
    nvm use 8.0.0
    gulp "test" --travis
elif [ "$RUNTEST" == "backend" ]; then
    backend
    flake8
    tox -e fast
    tox -e missing-migrations
elif [ "$RUNTEST" == "acceptance" ]; then
    frontend
    backend
    source $HOME/.nvm/nvm.sh
    nvm use 8.0.0
    export DISPLAY=:99.0
    sh -e /etc/init.d/xvfb start &
    sleep 3
    export HEADLESS_CHROME_BINARY=/usr/bin/google-chrome-beta
    gulp test:acceptance
fi
