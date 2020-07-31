#!/usr/bin/env bash

set -e

docker build -t cfgov-deployable-zipfile-builder docker/deployable-zipfile

docker run \
  --rm \
  -it \
  -u $(id -u):$(id -g) \
  -v $(pwd):/cfgov \
  cfgov-deployable-zipfile-builder ./_build.sh
