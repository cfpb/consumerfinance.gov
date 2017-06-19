#!/bin/bash
source /usr/local/homebrew/bin/virtualenvwrapper.sh

# reset the world
docker-machine rm cfgov -y
deactivate cfgov-refresh
rmvirtualenv cfgov-refresh
rm -rf ~/Library/Caches/pip
rm -rf node_modules
rm -rf .env

# run our standard setup
source load-env.sh
source setup.sh
sleep 10
source refresh-data.sh
