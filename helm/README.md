# CFGOV Helm Chart

# build-images.sh
In the main `consumerfinance.gov` directory, there is [`build-images.sh`](../build-images.sh).
This script will build the required images for Kubernetes. **You must run this 
script as a pre-requisite to `helm-install.sh`. `build-images.sh` takes 1 argument, 
which is the tag. Valid values are `local` and `prod`.

## Usage

    ./build-images.sh  # Same as local
    ./build-images.sh local
    ./build-images.sh prod

# helm-install.sh
In the main `consumerfinance.gov` directory, there is [`helm-install.sh`](../helm-install.sh). 
This script is built to inject environment variables into the provided 
override yamls in [`overrides`](overrides).

## Usage
In all cases, make sure you have built images via `build-images.sh`.
Arguments passed in to `helm-install.sh`, should be a spaced separated list of override yamls.
If no arguments are provided, it includes [`local.yaml`](overrides/local.yaml)
and [`services.yaml`](overrides/services.yaml).

### Default Execution
The following commands are equivalent

    ./helm-install
    ./helm-install helm/overrides/local.yaml helm/overrides/services.yaml

If you provide any arguments, it will only include those provided.

### Local (no services)

    ./helm-install helm/overrides/local.yaml

### Prod (with services)

    # ClusterIP
    ./helm-install helm/overrides/prod.yaml helm/overrides/services.yaml

    # LoadBalancer - Port 8000
    ./helm-install helm/overrides/prod.yaml helm/overrides/services.yaml helm/overrides/lb8000.yaml

## Remove Helm Release
To remove a cfgov release installed with [`./helm-install`](../helm-install.sh),
run the following command in the correct namespace

    helm uninstall cfgov


## Provided Overrides
* [`local.yaml`](overrides/local.yaml) - Local dev stack (minus services)
* [`services.yaml`](overrides/services.yaml) - Services Stack (Postgres, ElasticSearch, Kibana)
* [`prod.yaml`](overrides/prod.yaml) - Prod stack (minus services)
* [`lb8000.yaml`](overrides/lb8000.yaml) - LoadBalancer bound to port 8000 (useful for local prod stack, already part of [`local.yaml`](overrides/local.yaml))
* [`init-sleep.yaml`](overrides/init-sleep.yaml) - Sleep cfgov initContainer to infinity (debug use)
* [`sleep.yaml`](overrides/sleep.yaml) - Sleep cfgov container to infinity (debug use)

### Debug Examples

    # Sleep initContainer (use for makemigrations, migrations, etc)
    ./helm-install.sh helm/overrides/local.yaml helm/overrides/services.yaml helm/overrides/init-sleep.yaml

    # Prod and Services Stack with CFGOV LoadBalancer bound to port 8000 (Local Prod Testing)
    ./helm-install.sh helm/overrides/prod.yaml helm/overrides/services.yaml helm/overrides/lb8000.yaml helm/overrides/sleep.yaml


# Override Values
TODO: Add Table with commonly overridden values.
