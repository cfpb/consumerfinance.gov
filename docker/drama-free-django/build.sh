#!/usr/bin/env bash

set -e

docker build --build-arg "CACHEBUST=$(date)" -t cfgov-dfd-builder docker/drama-free-django

docker run \
  --rm \
  -u $(id -u):$(id -g) \
  -v $(pwd):/cfgov \
  cfgov-dfd-builder ./_build.sh
