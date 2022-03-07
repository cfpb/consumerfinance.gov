#!/bin/sh

TAG=$1
if [ -z "$TAG" ]; then
  TAG="local"
fi

case "$TAG" in
  "local")
    TARGET="dev"
    ;;
  "prod")
    TARGET="prod"
    ;;
  *)
    echo "Tag must be 'local' or 'prod'"
    exit 2
esac

echo "Building cfgov_docs..."
docker build . -f docker/docs/Dockerfile -t cfgov_docs &
echo "Building cfgov_python:$TAG"
docker build . --target "cfgov-$TARGET" -t "cfgov_python:$TAG"
