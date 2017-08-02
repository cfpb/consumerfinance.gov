#!/bin/bash

eval $(docker-machine env cfgov)

docker-compose stop
docker-machine stop cfgov
