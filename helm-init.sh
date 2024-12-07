#!/bin/bash

# Function to display usage
usage() {
    echo "Usage: $0 [--release <release-name>]"
    exit 1
}

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --release)
            RELEASE_NAME="$2"
            shift
            ;;
        *)
            usage
            ;;
    esac
    shift
done

if ! command -v helm &> /dev/null; then
    echo "helm could not be found. Please install it before running this script."
    exit 1
fi


if ! command -v kubectl &> /dev/null; then
    echo "kubectl could not be found. Please install it before running this script."
    exit 1
fi

CLUSTER=$(kubectl config current-context)

if [ -z "$CLUSTER" ]; then
    echo "No Kubernetes cluster is currently configured. Please configure a cluster before running this script."
    exit 1
fi

echo $CLUSTER

if [[ "$CLUSTER" != "docker-desktop" &&  "$CLUSTER" != "colima" ]]; then
    echo ""
    echo -e "This script is intended to be run on a local Kubernetes cluster (i.e. docker-desktop or colima). The current cluster is $CLUSTER."
    echo -e "Your current cluster is $CLUSTER." 
    echo -e "Please switch to docker-desktop or colima before running this script."
    echo ""
    echo ""
    echo "Exiting helm-init"
    exit 1
fi

HELM_DIR="./helm"

if [ -n "$RELEASE_NAME" ]; then
    echo "Release name: $RELEASE_NAME"
else
    echo "No release name provided."
    echo "Using default release name: 'cfgov'"
    RELEASE_NAME="cfgov"
fi

if [ -d "./cfgov/apache" ]; then
    echo "Moving ./cfgov/apache to $HELM_DIR"
    cp -r ./cfgov/apache $HELM_DIR
else
    echo "Directory ./cfgov/apache does not exist."
    exit 1
fi

if [! -d ./helm/charts]; then
    echo "Building Helm charts..."
    helm repo update
    helm dependency build $HELM_DIR
else
    if [ -z $SKIP_DEP_UPDATE ]; then
        echo "Updating Helm dependencies..."
        helm dependency update $HELM_DIR
    fi
fi 

helm upgrade --install $RELEASE_NAME $HELM_DIR -f $HELM_DIR/values.yaml

rm -r $HELM_DIR/apache

