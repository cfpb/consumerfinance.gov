#!/usr/bin/env bash

container_id=$(
    docker run \
        -d \
        -v `pwd`:/cfgov \
        centos:6 \
        /bin/bash -c "/cfgov/docker/drama-free-django/_build.sh && /cfgov/docker/drama-free-django/_test.sh"
)

docker logs -f $container_id
