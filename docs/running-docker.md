# Running in Docker

First, follow
[the Docker installation instructions](installation.md#docker-based-installation)
to setup your Docker environment and create the project Docker containers.

We use [`docker-compose`](https://docs.docker.com/compose/reference/overview/)
to run an Elasticsearch container, a PostgreSQL container, an Apache container,
and Django in a Python container.

All of these containers are configured in our
[`docker-compose.yml` file](https://github.com/cfpb/consumerfinance.gov/blob/main/docker-compose.yml).
See the [Docker documentation](https://docs.docker.com/compose/compose-file/)
for more about the format and use of this file.

The following URLs are mapped to your host from the containers:

- Access consumerfinance.gov directly running in the Python container: http://localhost:8000/
- Access Apache proxying to the Python container: http://localhost:8080/
- Access Elasticsearch: http://localhost:9200/

To build and run the containers for the first time, run:

```bash
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

- Python: `docker-compose exec python sh`
- Elasticsearch: `docker-compose exec elasticsearch bash`
- PostgreSQL: `docker-compose exec postgres bash`

## Update/Change Python MAJOR.MINOR Version

The [first line](https://github.com/cfpb/consumerfinance.gov/tree/main/Dockerfile)
of `Dockerfile` sets the base Python Interpreter version for all `cfgov`
images. Our current pattern is `python:MAJOR.MINOR-alpine` for the base image.
This allows us to rapidly incorporate `PATCH` versions without the need
for explicit commits.

### Updating `PATCH` version locally

To update the `PATCH` version on your local Docker, replace `<MAJOR.MINOR>`
with your target and run:

```bash
PYTHONVERSION=<MAJOR.MINOR>; \
  docker pull python:${PYTHONVERSION}-alpine && \
  docker-compose build --no-cache python
```

## Update Python dependencies

If the Python package requirements files have changed,
you will need to stop `docker-compose` (if it is running)
and rebuild the Python container using:

```bash
docker-compose up --build python
```

## Work on satellite apps

See [“Using Docker” on the Related Projects page](related-projects.md#using-docker).

## Attach for debugging

If you have inserted a [PDB breakpoint](https://docs.python.org/3/library/pdb.html) in your code
and need to interact with the running Django process when the breakpoint is reached
you can run [`docker attach`](https://docs.docker.com/engine/reference/commandline/attach/):

```bash
docker attach consumerfinancegov-python-1
```

When you're done, you can detach with `Ctrl+P Ctrl+Q`.

!!! note

    `docker attach` takes the specific container name or ID.
    Yours may or may not be `consumerfinancegov-python-1`.
    To verify, use `docker container ls`
    to get the Python container's full name or ID.

!!! note

    `docker attach` will ONLY work with the dev image, not prod.

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
- all OS, Python, and JS dependencies for building and running cf.gov
- procedures for executing Django `collectstatic` and `yarn`-based frontend build process

### How do I use it?

#### Just Docker

If you just want to build the image:

```bash
docker build . -t your-desired-image-name
```

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

1. Load the `cfgov` database (optional). If you do not already have a running
   `cfgov` database, you will need to download and load it from within the container.

   ```bash
   docker-compose exec python sh

   # Once in the container...
   export CFGOV_PROD_DB_LOCATION=<database-dump-url>
   ./refresh-data.sh
   ```

1. Browse to your new local cf.gov site:

   http://localhost:8080 (Apache)

   Or directly to Gunicorn running Django:

   http://localhost:8000 (Gunicorn)

1. Adjust an Apache [`cfgov/apache`](https://github.com/cfpb/consumerfinance.gov/tree/main/cfgov/apache)
   config and restart the Apache container.

   ```bash
   docker-compose restart apache
   ```

1. Switch back to the development Compose setup.

   ```bash
   docker-compose rm -sf python
   docker-compose up --build python
   ```

### How does it work?

This project heavily utilizes
"[multi-stage builds](https://docs.docker.com/develop/develop-images/multistage-build/)".

There are a few layers at work here, with the hierarchy represented by the list structure:

- `python`, the base Python layer for building up any further layers.
  It includes OS and Python-level application requirements.
- `node-builder`, a Node-based image that runs our frontend build.
- `dev`, based on `python`, which copies frontend assets from `node-builder`,
  sets up some initial data, and runs Django with `local` settings via
  `runserver` on port 8000.
- `prod`, based on `python`, which copies frontend assets from `node-builder`,
  and runs the application with `production` settings via Gunicorn on
  port 8000.
