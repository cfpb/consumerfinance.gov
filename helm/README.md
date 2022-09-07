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
**NOTE:** It is *highly* recommended to install `ingress-nginx` to gain
access to the application via `Ingress`. You can find instructions for this
at the bottom of the document under [`ingress-nginx`](#ingress-nginx).

In the main `consumerfinance.gov` directory,
there is [`helm-install.sh`](../helm-install.sh).
This script is built to inject environment variables into the provided
override YAMLs in [`overrides`](overrides).

## Flags and Environment Variables
`helm-install.sh` is quite flexible in what you can configure via
Flags and Environment Variables.

It is highly recommended to set these variables inline when calling
`helm-install.sh`, as follows:

    SKIP_WAIT=y ./helm-install.sh

If you want to set a variable on your terminal session, you may:

    export SKIP_DEP_UPDATE=y
    ./helm-install.sh

You can clear a terminal session variable using `unset`

    unset SKIP_DEP_UPDATE
    ./helm-install.sh

**NOTE:** `helm-install.sh` will **ALWAYS** source `.env` if it exists.
If you have a variable set in `.env`, `unset` will not work for that variable.

### Flags
Flags are treated as `True` if the corresponding
Environment Variable is set to any value beyond empty string,
including `False`. Use `unset VARIABLE` to clear a set variable.

| Variable                | Description                                                                |
|-------------------------|----------------------------------------------------------------------------|
| `ES_ENABLE_CHART_TESTS` | Enable ElasticSearch Chart Tests                                           |
| `SKIP_WAIT`             | Skips `--wait`                                                             |
| `CREATE_NAMESPACE`      | Create namespace if it doesn't exist. Used in conjunction with `NAMESPACE` |
| `RUN_CHART_TESTS`       | Run `helm test ${RELEASE}` after deployment. Ignores `SKIP_WAIT`.          |
| `SKIP_DEP_UPDATE`       | Skip `helm dependency update` for faster iteration                         |

### Environment Variables
Environment Variables **need** a valid value to be set.

| Variable        | Description                                       |
|-----------------|---------------------------------------------------|
| `RELEASE`       | Set the release name.<br/>Default is `cfgov`.     |
| `NAMESPACE`     | Override the namespace for the release.           |
| `IMAGE`         | Set the `repository/image` for the release.       |
| `TAG`           | Set the image `tag` for the release.              |
| `WAIT_TIMEOUT`  | Set the `--wait` timeout.<br/>Default is `10m0s`  |

## Usage
In all cases, make sure you have built images via `build-images.sh`.
Arguments passed in to `helm-install.sh`, should be a spaced separated list
of paths to override YAMLs or `--set` overrides.

If no arguments are provided, it includes
[`local-dev.yaml`](overrides/local-dev.yaml),
[`dev-vars.yaml`](overrides/dev-vars.yaml), and
[`services.yaml`](overrides/services.yaml).

### Default Execution
The following commands are equivalent

    ./helm-install.sh
    ./helm-install.sh helm/overrides/local-dev.yaml helm/overrides/dev-vars.yaml helm/overrides/services.yaml

If you provide any arguments, it will only include those provided.

### Local (no services)

    ./helm-install.sh helm/overrides/local-dev.yaml helm/overrides/dev-vars.yaml

    # Using --set with override files
    ./helm-install.sh helm/overrides/local-dev.yaml helm/overrides/dev-vars.yaml helm/overrides/services.yaml --set image.tag=my-image-tag

    # With LoadBalancer for cfgov service
    ./helm-install.sh helm/overrides/local-dev.yaml helm/overrides/dev-vars.yaml helm/overrides/cfgov-lb.yaml

### Local Prod (with Dev Vars and services)

    # ClusterIP
    ./helm-install.sh helm/overrides/local-prod.yaml helm/overrides/dev-vars.yaml helm/overrides/services.yaml

    # LoadBalancer - CFGOV Port 8000, PSQL Port 5432, ES Port 9200, Kibana Port 5601
    ./helm-install.sh helm/overrides/local-prod.yaml helm/overrides/dev-vars.yaml helm/overrides/services.yaml helm/overrides/load-balancer.yaml

### EKS (with Dev Vars, GHCR Image, and services)

    NAMESPACE=my-namespace IMAGE=ghcr.io/cfpb/consumerfinance.gov TAG=latest \
      ./helm-install.sh \
      helm/overrides/dev-vars.yaml \
      ./helm/overrides/services.yaml \
      ./helm/overrides/eks.yaml

## Remove Helm Release
To remove a cfgov release installed with [`./helm-install`](../helm-install.sh),
run the following command in the correct namespace

    helm uninstall cfgov


## Provided Overrides
* [`local-dev.yaml`](overrides/local-dev.yaml) - Local dev stack (minus services)
* [`local-prod.yaml`](overrides/local-prod.yaml) - Local Prod stack (minus services)
* [`dev-vars.yaml`](overrides/dev-vars.yaml) - Dev Environment Variables
* [`services.yaml`](overrides/services.yaml) - Services Stack (Postgres, ElasticSearch, Kibana)
* [`cfgov-lb.yaml`](overrides/cfgov-lb.yaml) - Sets CFGOV Service to LoadBalancer with Port 8000
* [`load-balancer.yaml`](overrides/load-balancer.yaml) - Sets all service types to `LoadBalancer` (includes services, if enabled)
* [`init-sleep.yaml`](overrides/init-sleep.yaml) - Sleep cfgov initContainer to infinity (debug use)
* [`sleep.yaml`](overrides/sleep.yaml) - Sleep cfgov container to infinity (debug use)

### Debug Examples

    # Sleep initContainer (use for makemigrations, migrations, etc)
    ./helm-install.sh helm/overrides/local-dev.yaml helm/overrides/dev-vars.yaml helm/overrides/services.yaml helm/overrides/init-sleep.yaml

    # Prod and Services Stack with CFGOV LoadBalancer bound to port 8000 (Local Prod Testing)
    ./helm-install.sh helm/overrides/local-prod.yaml helm/overrides/dev-vars.yaml helm/overrides/services.yaml helm/overrides/cfgov-lb.yaml helm/overrides/sleep.yaml


# Chart Override Values
The actual Chart Value overrides.
TODO: Add Table with commonly overridden values.


# CronJobs
To make a new
[Kubernetes CronJob](https://kubernetes.io/docs/tasks/job/automated-tasks-with-cron-jobs/)
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
```

The following shows the all the available values and default values
for a cronJob object.

```yaml
- name: ""  # There is no default for name, this is required
  includeEnv: true  # includes the same volumes and environment variables as the main application container
  image:  # ONLY define if different from cfgov_python
    repository: cfogv_python  # default is the chart image repository
    tag: ""  # default is the chart image tag
  successfulJobsHistoryLimit: 1  # default
  failedJobsHistoryLimit: 1  # default
  schedule: "@daily"  # default
  suspend: false  # default
  restartPolicy: OnFailure  # default
  command:  # there is no default for command, this is required
    - "some-exec"
  args:  # there is no default for args, this is required
    - "space"
    - "separated"
    - "arguments"
  env:  # default is empty (not defined), but can define extra cronjob only environment variables as follows
    - name: MY_CRONJOB_ENV
      value: "MY_CRONJOB_ENV_VALUE"
```

# Manually Loading Data
To manually load data (such as `test.sql.gz`), deploy the Helm chart as normal.
You can wait for it to finish deploying, or not. Scale the main deployment to 0.

    kubectl scale deployment --replicas=0 cfgov

Once the main container has terminated, expose the Postgres and ElasticSearch
ports via port-forwarding. This is a blocking command, so you will need to
use multiple terminals (or use OpenLens). The will need to be exposed on their
respective ports (or update your `.env` accordingly).

    kubectl port-forward service/cfgov-postgresql 5432:5432
    kubectl port-forward service/cfgov-elasticsearch-master 9200:9200

Ensure you source your `.env` file, where it will set the `PG*` and `ES`
environment variables to `localhost`. Activate your virtual environment locally
as well.

    source .env  # Source .env file
    source venv/bin/activate  # Activate your virtualenv (however you do it)

Now you can run `./refresh-data.sh` to load your data.

    ./refresh-data.sh test.sql.gz

Once this has completed, scale the main deployment back up.

    kubectl scale deployment --replicas=1 cfgov

The main container should be created, and skip migrations
(assuming a user was created `SELECT COUNT(*) FROM auth_user`).
The main container should now be loaded with Postgres and ElasticSearch with
your manually loaded data.


# `ingress-nginx`
We use `ingress-nginx` as a cluster wide proxy to be able to map
`*.localhost` to multiple deployments (CFGOV, Grafana, etc) locally. To deploy
`ingress-nginx` to your local Kubernetes, run the following (change the ports
that the services binds to on localhost if needed, default is 80 and 443):

    helm upgrade --install ingress-nginx ingress-nginx \
      --set controller.service.ports.http=80 \
      --set controller.service.ports.https=443 \
      --repo https://kubernetes.github.io/ingress-nginx \
      --namespace ingress-nginx --create-namespace

This will allow us to access the application via
[http://\<release\>.localhost](http://<release>.localhost).
This enables ingress to mimic Ambassador `Mapping`'s locally.

*NOTE:* You will need to add the http port to the URL if you change
from 80.

Example:
  * default -> [http://cfgov.localhost](http://cfgov.localhost)
  * RELEASE=my-test -> [http://my-test.localhost](http://my-test.localhost)


# AWS CLI
To use the AWS CLI, the chart must be deployed with `$HOME/.aws` mounted,
or with keys and tokens passed in via environment variables or mounted in
the correct files within `/root/.aws` for `local` image, or `/var/www/.aws`
for the `prod` image. You can also mount the secrets to a different path
and set `AWS_CONFIG_FILE` and `AWS_SHARED_CREDENTIALS_FILE` variables,
pointing to the appropriate files. Additionally, you must have the
`AWS_PROFILE` env variable set on your local AWS configuration in order for
the CLI to use your credentials within the container.  More info on AWS CLI
Environment Variables can be found
[here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html).

Currently, the `local-dev.yaml` override will mount your `.aws` directory
to the containers for local development. This directory is mounted to
`/var/run/secrets/.aws`, then `AWS_CONFIG_FILE` and
`AWS_SHARED_CREDENTIALS_FILE` are set to the appropriate files within that
directory. To make use of AWS CLI in the containers locally, you will need
to run your `gimme-aws-creds` in your local terminal to get valid credentials
locally. AWS CLI will then work within the containers.

## Testing

To run tests in helm use `helm test <release_name>`.

To add new tests, follow the template provided by Helm in the
[Example Test Section](https://helm.sh/docs/topics/chart_tests/#example-test)
of the [Helm Chart Tests](https://helm.sh/docs/topics/chart_tests/)
documentation.

To exclude certain tests from running use
`helm test --filter strings name=<test_name>`. However, you can disable tests
from within in the `values.yaml` but **only** for tests that the charts have
added (i.e. the ElasticSearch Chart and Postgres Chart). You will need to
look up that chart's respective documentation for how to do that.

More can be found on Helm Chart Tests
[here](https://helm.sh/docs/topics/chart_tests/) or by running
`helm test --help`.


## TODO
In production, an AWS Service Account is used, and its credentials are
mounted within the containers to `/var/run/secrets/.aws`, then
`AWS_CONFIG_FILE` and `AWS_SHARED_CREDENTIALS_FILE` are set to the appropriate
files within that directory.
