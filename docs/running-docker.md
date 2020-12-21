# Running in Docker

First, follow
[the Docker installation instructions](../installation/#docker-based-installation)
to setup your Docker environment and create the project Docker containers.

We use [`docker-compose`](https://docs.docker.com/compose/reference/overview/)
to run an Elasticsearch container, a PostgreSQL container,
and Django in a Python container.
There is also a container serving the documentation.

All of these containers are configured in our
[`docker-compose.yml` file](https://github.com/cfpb/consumerfinance.gov/blob/main/docker-compose.yml).
See the [Docker documentation](https://docs.docker.com/compose/compose-file/)
for more about the format and use of this file.

The following URLs are mapped to your host from the containers:

- Access consumerfinance.gov running in the Python container: http://localhost:8000/
- Access Elasticsearch: http://localhost:9200/
- View this documentation: http://localhost:8888/

To build and run the containers for the first time, run:

```bash
docker network create cfgov
docker-compose up
```


## Environment variables

Environment variables from your `.env` file are sourced
when the Python container starts
and when you [access the running Python container](#access-a-containers-shell).
Your local shell environment variables, however,
are not visible to applications running in Docker.
To add new environment variables, simply add them to the `.env` file,
stop docker-compose with Ctrl+C,
and start it again with `docker-compose up`.


## Commands that must be run from within the Python container

Django `manage.py` commands can only be run after you've
[opened up a shell in the Python container](#access-a-containers-shell).
From there, commands like `cfgov/manage.py migrate` should run as expected.

The same goes for scripts like `./refresh-data.sh` and `./initial-data.sh` —
they will work as expected once you’re inside the Python container.


## Access a container’s shell

- Python: `docker-compose exec python bash`
- Elasticsearch: `docker-compose exec elasticsearch bash`
- PostgreSQL: `docker-compose exec postgres bash`


## Update Python dependencies

If the Python package requirements files have changed,
you will need to stop `docker-compose` (if it is running)
and rebuild the Python container using:

```bash
docker-compose up --build python
```


## Work on satellite apps

See [“Using Docker” on the Related Projects page](../related-projects/#using-docker).


## Attach for debugging

If you have inserted a [PDB breakpoint](https://docs.python.org/3/library/pdb.html) in your code
and need to interact with the running Django process when the breakpoint is reached
you can run [`docker attach`](https://docs.docker.com/engine/reference/commandline/attach/):

```bash
docker attach consumerfinancegov_python_1
```

When you're done, you can detach with `Ctrl+P Ctrl+Q`.

!!! note
    `docker attach` takes the specific container name or ID. 
    Yours may or may not be `consumerfinancegov_python_1`. 
    To verify, use `docker container ls` 
    to get the Python container's full name or ID.


## Useful Docker commands

For `docker-compose` commands,
`[SERVICE]` is the service name that is defined in `docker-compose.yml`.

For `docker` commands, `[CONTAINER]` is the container name displayed with `docker ps`.

- [`docker ps`](https://docs.docker.com/engine/reference/commandline/ps/)
    will list all containers.
- [`docker logs [CONTAINER]`](https://docs.docker.com/engine/reference/commandline/logs/)
    will print the logs of a container.
- [`docker top [CONTAINER]`](https://docs.docker.com/engine/reference/commandline/top/)
    will display the running processes in a container.
- [`docker-compose build [SERVICE]`](https://docs.docker.com/compose/reference/build/)
    will build any of our configured containers.


## Production-like Docker Image

This repository includes a "production-like" Docker image, created for
experimenting with how cf.gov _could_ be built and run as a Docker
container in production.

This includes:

- all relevant `consumerfinance.gov` source code
- all OS, Python, and JS dependencies for building and running the cf.gov webapp
- procedures for executing Django `collectstatic` and `yarn`-based frontend build process
- an Apache HTTPD webserver with `mod_wsgi`, run with configs in `consumerfinance.gov`

### How do I use it?

#### Just Docker

If you just want to build the image:

```bash
docker build . --build-arg scl_python_version=rh-python36 -t your-desired-image-name
```

**Note:** The `scl_python_version` build arg specifies which
[Python Software Collection](https://www.softwarecollections.org/en/scls/?search=python)
version you'd like to use. We've tested this against `rh-python36`.

#### Docker Compose

You can also launch the full cf.gov stack locally via `docker-compose`. This setup is
a nice way to test out new Apache config changes. It includes volumes that mount your
local checkout `cfgov/apache` config directories into the container, allowing you to
change configs locally without having to rebuild the image each time.

1. Launch the stack.

    ```bash
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build
    ```

    This creates a container running cf.gov on Python, as well as
    Postgres and Elasticsearch containers, much like the development environment.

1. Load the `cfgov` database (optional).  If you do not already have a running
    `cfgov` database, you will need to download and load it from within the container.

    ```bash
    docker-compose exec python bash

    # Once in the container...
    export CFGOV_PROD_DB_LOCATION=<database-dump-url>
    ./refresh-data.sh
    ```

1. Browse to your new local cf.gov site.

    http://localhost:8000


1. Adjust an Apache [`cfgov/apache`](https://github.com/cfpb/consumerfinance.gov/tree/main/cfgov/apache)
   config and reload Apache (optional).

    ```bash
    docker-compose exec python bash

    # Once in the container...
    httpd -d ./cfgov/apache -k restart
    ```

1. Switch back to the development Compose setup.

    ```bash
    docker-compose rm -sf python
    docker-compose up --build python
    ```

#### Jenkins CI + Docker Swarm

This repo also includes a Docker Swarm-compatible Compose file
(`docker-stack.yml`).
This file is intended for use with the project's `Jenkinsfile`
[multibranch build pipeline](https://jenkins.io/doc/tutorials/build-a-multibranch-pipeline-project/).
It follows a standard Docker build/scan/push workflow,
optionally deploying to our Docker Swarm cluster.

### How does it work?

The production image extends the development image. If you look at the `Dockerfile`, this is spelled out by the line:

```
FROM cfgov-dev as cfgov-prod
```

Both 'cfgov-dev' and 'cfgov-prod' are called "[build stages](https://docs.docker.com/develop/develop-images/multistage-build/)". That line means, "create a new stage, starting from cfgov-dev, called cfgov-prod".

From there, we:

- Install SCL-based Apache HTTPD, and the `mod_wsgi` version appropriate for our chosen `scl_python_version`.
- Run frontend.sh, Django's collectstatic command, and then *uninstall* node and yarn.
- Set the default command on container startup to `httpd -d ./cfgov/apache -D FOREGROUND`, which runs Apache using
    the [configuration in consumerfinance.gov](https://github.com/cfpb/consumerfinance.gov/tree/main/cfgov/apache), in the
    foreground (typical when running Apache in a container).
