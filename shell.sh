#!/bin/bash

docker ps > /dev/null 2>&1
if [ $? -ne 0 ]; then
    # If the user hasn't eval'ed the docker-machine env, do it for them
    if [ -z ${DOCKER_HOST} ] || 
       [ -z ${DOCKER_CERT_PATH} ] || 
       [ -z ${DOCKER_TLS_VERIFY} ] || 
       [ -z ${DOCKER_MACHINE_NAME} ]; then 
        docker-machine status > /dev/null 2>&1
        if [ $? -ne 0 ]; then
            echo "Can't find a working Docker, try running setup.sh"
            exit
        else
            eval $(docker-machine env) 
        fi
    fi
fi

if [ -z "$*" ]; then
    docker-compose exec python bash
else
    docker-compose exec python bash -c "$*"
fi
