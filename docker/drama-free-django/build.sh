#!/usr/bin/env bash

set -e

docker build --no-cache -t cfgov-dfd-builder docker/drama-free-django

docker run \
  --rm \
  -u $(id -u):$(id -g) \
  -v $(pwd):/cfgov \
  cfgov-dfd-builder ./_build.sh
