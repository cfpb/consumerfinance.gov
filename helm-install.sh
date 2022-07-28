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
  echo "Building dependency charts..."
  helm repo add bitnami https://charts.bitnami.com/bitnami
  helm repo add elastic https://helm.elastic.co/
  helm repo update
  helm dependency build ./helm/cfgov
else
  helm dependency update ./helm/cfgov
fi

# Parse overrides list
export PROJECT_DIR="$(dirname "$(realpath "$0")")"
if [ $# -eq 0 ]; then
  ARGS="$PROJECT_DIR/helm/overrides/local.yaml $PROJECT_DIR/helm/overrides/services.yaml $PROJECT_DIR/helm/overrides/cfgov-lb.yaml"
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

# Set release name
RELEASE=${RELEASE:-cfgov}
# Install/Upgrade cfgov release to current context namespace
# To install to different namespace, set context with namespace
# kubectl config set-context --current --namespace=<insert-namespace-name-here>
helm upgrade --install --wait --timeout=10m0s "${RELEASE}" $OVERRIDES \
  --set elasticsearch.clusterName="${RELEASE}-elasticsearch" \
  --set kibana.elasticsearchHosts="http://${RELEASE}-elasticsearch-master:9200" \
  ./helm/cfgov

# Cleanup temp files
for i in "${tempFiles[@]}"; do
  rm "$i"
done
