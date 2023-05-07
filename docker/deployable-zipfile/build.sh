#!/usr/bin/env bash

set -e

if [ ! -f "$(git rev-parse HEAD).zip" ]; then
  echo "build.sh requires a zip of the built static files named <current SHA>.zip."
  echo "You can produce one with 'yarn zip-artifact'."
  exit
fi

docker build -t cfgov-deployable-zipfile-builder docker/deployable-zipfile

docker run \
  --rm \
  -u $(id -u):$(id -g) \
  -v $(pwd):/cfgov \
  cfgov-deployable-zipfile-builder ./_build.sh
