#!/bin/bash

# reset the world
docker-machine rm cfgov -y
rm -rf .virtualenv
rm -rf ~/Library/Caches/pip
rm -rf node_modules
rm -rf .env

# new virtualenv
virtualenv .virtualenv
source .virtualenv/bin/activate

# run our standard setup
source load-env.sh
source setup.sh
sleep 10
source refresh-data.sh
