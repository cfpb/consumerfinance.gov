#!/bin/bash

# Flags
## Disable ES Chart Tests by default
ES_TEST_OVERRIDE="--set elasticsearch.tests.enabled=false"
if [ ! -z $ES_ENABLE_CHART_TESTS ]; then
  ES_TEST_OVERRIDE="--set elasticsearch.tests.enabled=true"
fi

## Option to skip --wait and set timeout
WAIT_TIMEOUT="--timeout=${WAIT_TIMEOUT:-10m0s}"
WAIT_OPT="--wait ${WAIT_TIMEOUT}"
if [ -z $RUN_CHART_TESTS ] && [ ! -z $SKIP_WAIT ]; then
  echo "WARNING: Skipping --wait!"
  WAIT_OPT=""
fi

## Namespace
NAMESPACE_OPT=""
if [ ! -z $NAMESPACE ]; then
  NAMESPACE_OPT="--namespace ${NAMESPACE}"
  if [ ! -z $CREATE_NAMESPACE ]; then
    NAMESPACE_OPT="${NAMESPACE_OPT} --create-namespace"
  fi
fi

## Image Option
if [ -z $IMAGE ]; then
  IMAGE=""
else
  IMAGE="--set image.repository=${IMAGE}"
fi

## Tag Option
if [ -z $TAG ]; then
  TAG=""
else
  TAG="--set image.tag=${TAG}"
fi

## Set release name
RELEASE=${RELEASE:-cfgov}

# Setup
## Get absolute path to helm-install.sh
realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}
## Get Project Dir path containing helm-install.sh
export PROJECT_DIR="$(dirname "$(realpath "$0")")"
## Set Default Args
DEFAULT_ARGS="${PROJECT_DIR}/helm/overrides/local-dev.yaml ${PROJECT_DIR}/helm/overrides/dev-vars.yaml ${PROJECT_DIR}/helm/overrides/services.yaml"
## Source .env, if it exists
if [ -f .env ]; then
  source .env
fi

# Prerequisites
## Ensure helm is installed and available via PATH
if ! command -v helm &> /dev/null; then
  echo "Helm not found in PATH. Please install helm (brew install helm) or add it to PATH."
  exit 1
fi

## Build Dependency Charts
if [ ! -d ./helm/cfgov/charts ]; then
  echo "Building dependency charts..."
  helm repo add bitnami https://charts.bitnami.com/bitnami
  helm repo add elastic https://helm.elastic.co/
  helm repo add opensearch https://opensearch-project.github.io/helm-charts/
  helm repo update
  helm dependency build ./helm/cfgov
else
  if [ -z $SKIP_DEP_UPDATE ]; then
    helm dependency update ./helm/cfgov
  fi
fi

# Generate Overrides
## Parse overrides list
if [ $# -eq 0 ]; then
  ARGS=${DEFAULT_ARGS}
else
  ARGS=$@
fi

## Separate --set from files, substitute Environment Variables in override files
tempFiles=()
unset PENDING_SET
OVERRIDES=""
for i in $ARGS; do
  if [ ! -z $PENDING_SET ]; then
    OVERRIDES="${OVERRIDES} --set ${i}"
    unset PENDING_SET
  elif [ "${i}" == "--set" ]; then
    PENDING_SET=true
  else
    tempFile=$(mktemp)
    envsubst < ${i} > "$tempFile"
    OVERRIDES="$OVERRIDES -f $tempFile"
    tempFiles+=($tempFile)
  fi
done

# Execute
## Install/Upgrade cfgov release
helm upgrade --install ${WAIT_OPT} \
  "${RELEASE}" ${NAMESPACE_OPT} ${OVERRIDES} ${IMAGE} ${TAG} \
  --set ingress.hosts[0].host="${RELEASE}.localhost" \
  --set elasticsearch.clusterName="${RELEASE}-elasticsearch" ${ES_TEST_OVERRIDE} \
  --set kibana.elasticsearchHosts="http://${RELEASE}-elasticsearch-master:9200" \
  ${PROJECT_DIR}/helm/cfgov

# Add these in for local SSL.
#  --set ingress.tls[0].secretName="${RELEASE}-tls" \  # local SSL
#  --set ingress.tls[0].hosts[0]="${RELEASE}.localhost" \  # local SSL

## Run chart tests, if RUN_CHART_TESTS is set
if [ ! -z $RUN_CHART_TESTS ]; then
  echo "Running chart tests against ${RELEASE}..."
  helm test "${RELEASE}"
fi

# Cleanup
## Remove temp files
for i in "${tempFiles[@]}"; do
  rm "$i"
done
