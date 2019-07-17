#!/usr/bin/env bash

docker run \
    -v `pwd`:/cfgov \
    -e PYTHONUNBUFFERED=1 \
    centos:6 \
    /bin/bash -c "/cfgov/docker/drama-free-django/_build.sh && /cfgov/docker/drama-free-django/_test.sh"
