#!/bin/bash

# Fail if any command fails.
set -e

# Define color codes for pretty output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

OUTPUT_FILE=$(mktemp)

# Check if helm is installed
if ! command -v helm &> /dev/null; then
    echo -e "${RED}Helm could not be found. Please install it before running this script.${NC}"
    exit 1
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}Kubectl could not be found. Please install it before running this script.${NC}"
    exit 1
fi

if ! docker images -q --filter=reference='cfgov' | grep -q .; then
    echo -e "${RED}Docker image 'cfgov' could not be found."
    docker build . -t cfgov
fi

if ! docker images -q --filter=reference='cfgov-apache' | grep -q .; then
    echo -e "${RED}Docker image 'cfgov-apache' could not be found."
    docker build ./cfgov/apache/. -t cfgov-apache
fi

# Get the current Kubernetes cluster context
CLUSTER=$(kubectl config current-context)

# Check if a Kubernetes cluster is configured
if [ -z "$CLUSTER" ]; then
    echo -e "${RED}No Kubernetes cluster is currently configured. Please configure a cluster before running this script.${NC}"
    exit 1
fi

echo -e "${GREEN}Current Kubernetes cluster: $CLUSTER${NC}"

# Check if the current cluster is a local cluster (docker-desktop or colima)
if [[ "$CLUSTER" != "docker-desktop" &&  "$CLUSTER" != "colima" ]]; then
    echo -e "${YELLOW}"
    echo -e "This script is intended to be run on a local Kubernetes cluster (i.e. docker-desktop or colima)."
    echo -e "Your current cluster is ${RED}$CLUSTER${YELLOW}."
    echo -e "Please switch to docker-desktop or colima before running this script."
    echo -e "${NC}"
    echo -e "${RED}Exiting helm-init${NC}"
    exit 1
fi

# Define the Helm directory
HELM_DIR="./helm"


# Check if the ./cfgov/apache directory exists
if [ -d "./cfgov/apache" ]; then
    echo -e "${GREEN}Moving ./cfgov/apache to $HELM_DIR${NC}"
    cp -r ./cfgov/apache $HELM_DIR
else
    echo -e "${RED}Directory ./cfgov/apache does not exist.${NC}"
    exit 1
fi

# Check if the ./helm/charts directory exists
if [ ! -d "./helm/charts" ]; then
    echo -e "${GREEN}Building Helm charts...${NC}"
    helm dependency update $HELM_DIR
    helm dependency build $HELM_DIR
else
    # Update Helm dependencies if SKIP_DEP_UPDATE is not set
    if [ -z "$SKIP_DEP_UPDATE" ]; then
        echo -e "${GREEN}Updating Helm dependencies...${NC}"
        helm dependency update $HELM_DIR
    fi
fi

# Upgrade or install the Helm release
echo -e "${GREEN}Upgrading/Installing Helm release...${NC}"
helm upgrade --install cfgov $HELM_DIR -f $HELM_DIR/values.local.yaml >> $OUTPUT_FILE 2>&1

# Remove the copied apache directory
echo -e "${GREEN}Cleaning up...${NC}"
rm -r $HELM_DIR/apache

echo -e "${GREEN}Helm initialization script completed successfully.${NC}"

cat $OUTPUT_FILE
rm $OUTPUT_FILE
