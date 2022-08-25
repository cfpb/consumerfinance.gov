#!/bin/bash

if [ -f .env ]; then
  source .env
fi

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
  if [ -z $SKIP_DEP_UPDATE ]; then
    helm dependency update ./helm/cfgov
  fi
fi

# Parse overrides list
export PROJECT_DIR="$(dirname "$(realpath "$0")")"
if [ $# -eq 0 ]; then
  ARGS="$PROJECT_DIR/helm/overrides/local.yaml $PROJECT_DIR/helm/overrides/services.yaml"
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

# Disable ES Chart Tests by default
# This should also be a pipeline parameter for deployments
ES_TEST_OVERRIDE="--set elasticsearch.tests.enabled=false"
if [ ! -z $ES_ENABLE_CHART_TESTS ]; then
  ES_TEST_OVERRIDE="--set elasticsearch.tests.enabled=true"
fi

# Option to skip --wait and set timeout
WAIT_TIMEOUT="--timeout=${WAIT_TIMEOUT:-10m0s}"
WAIT_OPT="--wait ${WAIT_TIMEOUT}"
if [ -z $RUN_CHART_TESTS ] && [ ! -z $SKIP_WAIT ]; then
  echo "WARNING: Skipping --wait!"
  WAIT_OPT=""
fi

# Namespace
NAMESPACE_OPT=""
if [ ! -z $NAMESPACE ]; then
  NAMESPACE_OPT="--namespace ${NAMESPACE}"
  if [ ! -z $CREATE_NAMESPACE ]; then
    NAMESPACE_OPT="${NAMESPACE_OPT} --create-namespace"
  fi
fi

# Set release name
RELEASE=${RELEASE:-cfgov}
# Install/Upgrade cfgov release to current context namespace
# To install to different namespace, set context with namespace
# kubectl config set-context --current --namespace=<insert-namespace-name-here>
helm upgrade --install ${WAIT_OPT} "${RELEASE}" ${NAMESPACE_OPT} ${OVERRIDES} \
  --set ingress.hosts[0].host="${RELEASE}.localhost" \
  --set elasticsearch.clusterName="${RELEASE}-elasticsearch" ${ES_TEST_OVERRIDE} \
  --set kibana.elasticsearchHosts="http://${RELEASE}-elasticsearch-master:9200" \
  ./helm/cfgov

# Add these in for local SSL.
#  --set ingress.tls[0].secretName="${RELEASE}-tls" \  # local SSL
#  --set ingress.tls[0].hosts[0]="${RELEASE}.localhost" \  # local SSL

# Run chart tests, if RUN_CHART_TESTS is set
if [ ! -z $RUN_CHART_TESTS ]; then
  echo "Running chart tests against ${RELEASE}..."
  helm test "${RELEASE}"
fi

# Cleanup temp files
for i in "${tempFiles[@]}"; do
  rm "$i"
done
