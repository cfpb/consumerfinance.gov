#!/bin/bash

# Fail if any command fails.
set -e

# Define color codes for pretty output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Check if helm is installed
if ! command -v helm &> /dev/null; then
    echo -e "${RED}Helm could not be found. Please install it before running this script.${NC}"
    exit 1
fi

# Define the release name and namespace
RELEASE_NAME="cfgov"
NAMESPACE="default"

# Uninstall the Helm release
echo -e "${GREEN}Uninstalling Helm release ${RELEASE_NAME}...${NC}"
helm uninstall $RELEASE_NAME --namespace $NAMESPACE

# Uninstall the PVCs for the PostgreSQL and OpenSearch pods
kubectl delete pvc data-cfgov-postgresql-0 --namespace $NAMESPACE
kubectl delete pvc opensearch-cluster-master-opensearch-cluster-master-0 --namespace $NAMESPACE

# Check if the uninstall was successful
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Helm release ${RELEASE_NAME} uninstalled successfully.${NC}"
else
    echo -e "${RED}Failed to uninstall Helm release ${RELEASE_NAME}.${NC}"
    exit 1
fi

# Optionally, delete the namespace if it was created specifically for this release
# echo -e "${GREEN}Deleting namespace ${NAMESPACE}...${NC}"
# kubectl delete namespace $NAMESPACE

echo -e "${GREEN}Helm uninstallation script completed successfully.${NC}"
