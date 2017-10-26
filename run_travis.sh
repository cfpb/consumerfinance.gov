#!/usr/bin/env bash

# Fail if any command fails.
set -e

# Set RUNTEST to the first argument if it's not set
if [ -z $RUNTEST ]; then
    RUNTEST=$1
fi

# Install frontend dependencies
install_frontend() {
    export CXX=clang++

    if [[ "$(node -v)" != 'v8.'* ]]; then
        curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.2/install.sh | bash
        source $HOME/.nvm/nvm.sh
        nvm install 8.0.0
    fi

    npm install -g gulp-cli

    chmod +x ./frontend.sh
    ./frontend.sh test
}

# Install backend dependencies
install_backend() {
    # Use .venv as the virtualenv path if not already defined.
    VIRTUALENV_PATH=".venv"

    # Create virtualenv if needed.
    if [ ! -e "$VIRTUALENV_PATH" ]; then
        printf "Creating virtualenv in %s\n" "$VIRTUALENV_PATH"
        virtualenv -p `which python2.7` "$VIRTUALENV_PATH"
    else
        printf "%s already exists\n" "$VIRTUALENV_PATH"
    fi

    source "$VIRTUALENV_PATH/bin/activate"

    # Install dependencies if provided.
    pip install -r requirements/travis.txt
}

echo "running $RUNTEST tests"
if [ "$RUNTEST" == "frontend" ]; then
    install_frontend
    gulp "test" --travis
elif [ "$RUNTEST" == "backend" ]; then
    install_backend
    flake8
    tox -e fast
    tox -e missing-migrations
elif [ "$RUNTEST" == "acceptance" ]; then
    install_frontend
    install_backend
    export DISPLAY=:99.0
    sh -e /etc/init.d/xvfb start &
    sleep 3
    export HEADLESS_CHROME_BINARY=/usr/bin/google-chrome-beta
    gulp test:acceptance
fi
