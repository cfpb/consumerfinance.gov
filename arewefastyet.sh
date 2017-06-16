#!/bin/bash

# reset the world
docker-machine rm cfgov -y
rm -rf .virtualenv
rm -rf ~/Library/Caches/pip
rn -rf node_modules

# new virtualenv
virtualenv .virtualenv
source .virtualenv/bin/activate

# run our standard setup
source setup.sh
sleep 10
source refresh-data.sh
