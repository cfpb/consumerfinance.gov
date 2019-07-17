#!/usr/bin/env bash

docker run -v `pwd`:/cfgov centos:6 /cfgov/docker/drama-free-django/_test.sh
