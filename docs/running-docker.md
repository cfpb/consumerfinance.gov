# Running in Docker

First, follow
[the Docker installation instructions](../installation/#docker-based-installation)
to setup your Docker environment and create the project Docker containers.

We use [`docker-compose`](https://docs.docker.com/compose/reference/overview/)
to run an Elasticsearch container, a PostgreSQL container, 
and Django in a Python 3.6 container. 
There is also a container serving the documentation. 

All of these containers are configured in our 
[`docker-compose.yml` file](https://github.com/cfpb/cfgov-refresh/blob/master/docker-compose.yml). 
See the [Docker documentation](https://docs.docker.com/compose/compose-file/) 
for more about the format and use of this file.

The following URLs are mapped to your host from the containers:

- Access cfgov-refresh running in the Python 3.6 container: http://localhost:8000/
- Access Elasticsearch: http://localhost:9200/
- View this documentation: http://localhost:8888/

To build and run the containers for the first time, run:

```bash
docker-compose up
```

### Environment variables

Environment variables from your `.env` file are sourced 
when the Python container starts
and when you [access the running Python container](#access-the-containers-shell). 
Your local shell environment variables, however, 
are not visible to applications running in Docker.
To add new environment variables, simply add them to the `.env` file, 
stop docker-compose with Ctrl+C, 
and start it again with `docker-compose up`.

### Access a container's shell

- Python 3.6: `docker-compose exec python3 bash`
- Elasticsearch: `docker-compose exec elasticsearch bash`
- PostgreSQL: `docker-compose exec postgres bash`

### Run Django management commands

Django `manage.py` commands can only be run after you've 
[opened up a shell in the Python container](](#access-the-containers-shell)). 
From there commands like `cfgov/manage.py migrate` should run as expected.

The same goes for scripts like `./refresh-data.sh` and `./initial-data.sh` —
they will work as expected once you're inside the container.

### Update Python dependencies

If the Python package requirements files have changed, 
you will need to stop `docker-compose` (if it is running) 
and rebuild the Python container using:

```
docker-compose up --build python3
```

### Work on satellite apps

See [Related Projects#Using Docker](../related-projects/#using-docker).

### Attach for debugging

If you have inserted a [PDB breakpoint](https://docs.python.org/3/library/pdb.html) in your code 
and need to interact with the running Django process when the breakpoint is reached 
you can run [`docker attach`](https://docs.docker.com/engine/reference/commandline/attach/):

- Python 3.6: `docker attach cfgov-refresh_python3_1`

When you're done, you can detach with `Ctrl+P Ctrl+Q`.


### Useful Docker commands

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

# Production-like Docker Image

This repository includes a "production-like" Docker image, created for
experimenting with how cf.gov _could_ be built and run as a Docker
container in production.

This includes:

- all relevant `cfgov-refresh` source code
- all OS, Python, and JS dependencies for building and running the cf.gov webapp
- procedures for executing Django `collectstatic` and `yarn`-based frontend build process
- an Apache HTTPD webserver with `mod_wsgi`, run with configs in `cfgov-refresh`

## How do I use it?

### Just Docker

If you just want to build the image:

```bash
docker build . --build-arg scl_python_version=rh-python36 -t your-desired-image-name
```

**Note:** The `scl_python_version` build arg specifies which
[Python Software Collection](https://www.softwarecollections.org/en/scls/?search=python)
version you'd like to use. We've tested this against `rh-python36`.

### Docker Compose

You can also launch the full cf.gov stack locally via `docker-compose`. This setup is
a nice way to test out new Apache config changes. It includes volumes that mount your
local checkout `cfgov/apache` config directories into the container, allowing you to
change configs locally without having to rebuild the image each time.

1. Launch the stack.

    ```bash
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build
    ```

    This creates a container running Python 3.6 version of cf.gov, as well as
    Postgres and Elasticsearch containers, much like the development environment.

1. Load the `cfgov` database (optional).  If you do not already have a running
    `cfgov` database, you will need to download and load it from within the container.

    ```bash
    docker-compose exec python3 bash

    # Once in the container...
    export CFGOV_PROD_DB_LOCATION=<database-dump-url>
    ./refresh-data.sh
    ```

1. Browse to your new local cf.gov site.

    - Python 3.6: http://localhost:8000


1. Adjust an Apache [`cfgov/apache`](https://github.com/cfpb/cfgov-refresh/tree/master/cfgov/apache)
   config and reload Apache (optional).

    ```bash
    docker-compose exec python3 bash

    # Once in the container...
    httpd -d ./cfgov/apache -k restart
    ```

1. Switch back to the development Compose setup.

    ```bash
    docker-compose rm -sf python3
    docker-compose up --build python3
    ```


## How does it work?

The production image extends the development image. If you look at the `Dockerfile`, this is spelled out by the line:

```
FROM cfgov-dev as cfgov-prod
```

Both 'cfgov-dev' and 'cfgov-prod' are called "[build stages](https://docs.docker.com/develop/develop-images/multistage-build/)". That line means, "create a new stage, starting from cfgov-dev, called cfgov-prod".

From there, we:

- Install SCL-based Apache HTTPD, and the `mod_wsgi` version appropriate for our chosen `scl_python_version`.
- Run frontend.sh, Django's collectstatic command, and then *uninstall* node and yarn.
- Set the default command on container startup to `httpd -d ./cfgov/apache -D FOREGROUND`, which runs Apache using
    the [configuration in cfgov-refresh](https://github.com/cfpb/cfgov-refresh/tree/master/cfgov/apache), in the
    foreground (typical when running Apache in a container).
