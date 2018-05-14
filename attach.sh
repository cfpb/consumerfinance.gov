#!/bin/sh

docker ps > /dev/null 2>&1
if [ $? -ne 0 ]; then
    # If the user hasn't eval'ed the docker-machine env, do it for them
    if [ -z ${DOCKER_HOST} ] || 
       [ -z ${DOCKER_CERT_PATH} ] || 
       [ -z ${DOCKER_TLS_VERIFY} ] || 
       [ -z ${DOCKER_MACHINE_NAME} ]; then 
        docker-machine status > /dev/null 2>&1
        if [ $? -ne 0 ]; then
            echo "Can't find a working Docker -- please see our documentation:"
            echo ""
            echo "* Docker-based setup:"
            echo "    https://cfpb.github.io/cfgov-refresh/installation/#docker-compose-installation"
            echo ""
            echo "* Docker usage guide:"
            echo "    https://cfpb.github.io/cfgov-refresh/usage/#usage-docker"
            echo ""
            exit
        else
            eval $(docker-machine env) 
        fi
    fi
fi

docker attach cfgovrefresh_python_1
