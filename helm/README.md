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

    ./helm-install.sh
    ./helm-install.sh helm/overrides/local.yaml helm/overrides/services.yaml helm/overrides/cfgov-lb.yaml

If you provide any arguments, it will only include those provided.

### Local (no services)

    ./helm-install.sh helm/overrides/local.yaml

    # With LoadBalancer for cfgov service
    ./helm-install.sh helm/overrides/local.yaml helm/overrides/cfgov-lb.yaml

### Prod (with services)

    # ClusterIP
    ./helm-install.sh helm/overrides/prod.yaml helm/overrides/services.yaml

    # LoadBalancer - CFGOV Port 8000, PSQL Port 5432, ES Port 9200, Kibana Port 5601
    ./helm-install.sh helm/overrides/prod.yaml helm/overrides/services.yaml helm/overrides/load-balancer.yaml

## Remove Helm Release
To remove a cfgov release installed with [`./helm-install`](../helm-install.sh),
run the following command in the correct namespace

    helm uninstall cfgov


## Provided Overrides
* [`local.yaml`](overrides/local.yaml) - Local dev stack (minus services)
* [`services.yaml`](overrides/services.yaml) - Services Stack (Postgres, ElasticSearch, Kibana)
* [`prod.yaml`](overrides/prod.yaml) - Prod stack (minus services)
* [`cfgov-lb.yaml`](overrides/cfgov-lb.yaml) - Sets CFGOV Service to LoadBalancer with Port 8000
* [`load-balancer.yaml`](overrides/load-balancer.yaml) - Sets all service types to `LoadBalancer` (includes services, if enabled)
* [`init-sleep.yaml`](overrides/init-sleep.yaml) - Sleep cfgov initContainer to infinity (debug use)
* [`sleep.yaml`](overrides/sleep.yaml) - Sleep cfgov container to infinity (debug use)

### Debug Examples

    # Sleep initContainer (use for makemigrations, migrations, etc)
    ./helm-install.sh helm/overrides/local.yaml helm/overrides/services.yaml helm/overrides/init-sleep.yaml

    # Prod and Services Stack with CFGOV LoadBalancer bound to port 8000 (Local Prod Testing)
    ./helm-install.sh helm/overrides/prod.yaml helm/overrides/services.yaml helm/overrides/cfgov-lb.yaml helm/overrides/sleep.yaml


# Override Values
TODO: Add Table with commonly overridden values.


# Cron jobs

To make a new
[Kubernetes cron job](https://kubernetes.io/docs/tasks/job/automated-tasks-with-cron-jobs/)
based on our [CronJob template](cfgov/templates/cronjob.yaml),
add a new item to the cronJobs array in
[`cfgov/values.yaml`](cfgov/values.yaml).

For example, our Django
`clearsessions` management command runs in a cron job defined like this:

```yaml
- name: "clearSessions"
  schedule: "@daily"
  command:
    - "django-admin"
  args:
    - "clearsessions"
  restartPolicy: OnFailure
```
