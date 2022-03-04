#!/bin/sh

TARGET=$1
if [ -z "$TARGET" ]; then
  TARGET="local"
fi

case "$TARGET" in
  "local")
    ;;
  "prod")
    ;;
  *)
    echo "Tag must be 'local' or 'prod'"
    exit 2
esac

echo "Building cfgov_docs..."
docker build . -f docker/docs/Dockerfile -t cfgov_docs &
echo "Building cfgov_python:$TARGET"
docker build . --target "cfgov-$TARGET" -t "cfgov_python:$TARGET"
