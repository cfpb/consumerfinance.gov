#!/bin/sh

# If the user hasn't eval'ed the docker-machine env, do it for them
if [ -z ${DOCKER_HOST} ] || 
   [ -z ${DOCKER_CERT_PATH} ] || 
   [ -z ${DOCKER_TLS_VERIFY} ] || 
   [ -z ${DOCKER_MACHINE_NAME} ]; then 
    eval $(docker-machine env) 
fi
docker attach cfgovrefresh_python_1
