#!/usr/bin/env bash

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

echo "installing $RUNTEST dependencies"
if [ "$RUNTEST" == "frontend" ]; then
    frontend
elif [ "$RUNTEST" == "backend" ]; then
    backend
elif [ "$RUNTEST" == "acceptance" ]; then
    frontend
    backend
fi
