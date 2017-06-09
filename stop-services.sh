#!/bin/bash

eval $(docker-machine env cfgov)

docker-compose down
docker-machine stop cfgov
