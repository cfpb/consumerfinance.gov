#!/bin/bash

if [ -z "$VIRTUAL_ENV" ]; then
    source /usr/local/homebrew/bin/virtualenvwrapper.sh
    # reset the world
    docker-machine rm cfgov -y

    rmvirtualenv cfgov-refresh
    rm -rf ~/Library/Caches/pip
    rm -rf node_modules
    rm -rf .env

    # run our standard setup
    source load-env.sh
    source setup.sh
    sleep 10
    source refresh-data.sh
else
  echo you must 'deactivate' your virtualenv before running this
  exit 1
fi

source /usr/local/homebrew/bin/virtualenvwrapper.sh
# reset the world
docker-machine rm cfgov -y

rmvirtualenv cfgov-refresh
rm -rf ~/Library/Caches/pip
rm -rf node_modules
rm -rf .env

# run our standard setup
source load-env.sh
source setup.sh
sleep 10
source refresh-data.sh
