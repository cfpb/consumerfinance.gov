#!/bin/bash

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}

export PROJECT_DIR="$(dirname "$(realpath "$0")")"
if [ $# -eq 0 ]; then
  ARGS="$PROJECT_DIR/helm/overrides/local.yaml"
else
  ARGS=$@
fi

tempFiles=()
OVERRIDES=""
for i in $ARGS; do
  tempFile=$(mktemp)
  envsubst < ${i} > "$tempFile"
  OVERRIDES="$OVERRIDES -f $tempFile"
  tempFiles+=($tempFile)
done

if [ ! -d ./helm/cfgov/charts ]; then
  helm dependency build ./helm/cfgov
fi

helm upgrade --install cfgov $OVERRIDES ./helm/cfgov

for i in ${tempFiles[@]}; do
  rm "$i"
done
