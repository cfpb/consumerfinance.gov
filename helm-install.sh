#!/bin/bash

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}

# Ensure helm is installed and available via PATH
if ! command -v helm &> /dev/null; then
  echo "Helm not found in PATH. Please install helm (brew install helm) or add it to PATH."
  exit 1
fi

# Build Dependency Charts
if [ ! -d ./helm/cfgov/charts ]; then
  helm dependency build ./helm/cfgov
fi

# Parse overrides list
export PROJECT_DIR="$(dirname "$(realpath "$0")")"
if [ $# -eq 0 ]; then
  ARGS="$PROJECT_DIR/helm/overrides/local.yaml"
else
  ARGS=$@
fi

# Substitute Environment Variables in override files
tempFiles=()
OVERRIDES=""
for i in $ARGS; do
  tempFile=$(mktemp)
  envsubst < ${i} > "$tempFile"
  OVERRIDES="$OVERRIDES -f $tempFile"
  tempFiles+=($tempFile)
done

# Install/Upgrade cfgov release to current context namespace
# To install to different namespace, set context with namespace
# kubectl config set-context --current --namespace=<insert-namespace-name-here>
helm upgrade --install --create-namespace cfgov $OVERRIDES ./helm/cfgov

# Cleanup temp files
for i in ${tempFiles[@]}; do
  rm "$i"
done
