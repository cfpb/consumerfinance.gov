# Running in Docker

First, follow
[the Docker installation instructions](installation/#docker-compose-installation)
to setup your Docker environment and create the project Docker containers.

We use [`docker-compose`](https://docs.docker.com/compose/reference/overview/)
to run an Elasticsearch container, a PostgreSQL container, 
and Django in Python 2.7 and 3.6 containers. 
There is also a container serving the documentation. 

All of these containers are configured in our 
[`docker-compose.yml` file](https://github.com/cfpb/cfgov-refresh/blob/master/docker-compose.yml). 
See the [Docker documentation](https://docs.docker.com/compose/compose-file/) 
for more about the format and use of this file.

The following URLs are mapped to your host from the containers:

- Access cfgov-refresh running in the Python 2.7 container: http://localhost:8000/
- Access cfgov-refresh running in the Python 3.6 container: http://localhost:8333/
- Access Elasticsearch: http://localhost:9200/
- View this documentation: http://localhost:8888/

To build and run the containers for the first time, run:

```bash
docker-compose up
```

### Environment variables

Environment variables from your `.env` file are sourced 
when the Python containers start
and when you [access the running Python containers](#access-the-containers-shell). 
Your local shell environment variables, however, 
are not visible to applications running in Docker.
To add new environment variables, simply add them to the `.env` file, 
stop docker-compose with Ctrl+C, 
and start it again with `docker-compose up`.

### Access a container's shell

- Python 2.7: `docker-compose exec python2 bash`
- Python 3.6: `docker-compose exec python3 bash`
- Elasticsearch: `docker-compose exec elasticsearch bash`
- PostgreSQL: `docker-compose exec postgres bash`

### Run Django management commands

Django `manage.py` commands can only be run after you've 
[opened up a shell in one of the Python containers](](#access-the-containers-shell)). 
From there commands like `cfgov/manage.py migrate` should run as expected.

The same goes for scripts like `./refresh-data.sh` and `./initial-data.sh` —
they will work as expected once you're inside the container.

!!! note
    Because both Python containers use the same database (in the PostgreSQL container), 
    any management commands or scripts that operate on the database
    (like `migrate`, `refresh-data.sh`, and `initial-data.sh`)
    should only be run once in one of the two Python containers.

### Update Python dependencies

If the Python package requirements files have changed, 
you will need to stop `docker-compose` (if it is running) 
and rebuild the Python containers using:

```
docker-compose up --build python2 python3
```

### Work on satellite apps

See [Related Projects#Using Docker](../related-projects/#using-docker).

### Attach for debugging

If you have inserted a [PDB breakpoint](https://docs.python.org/3/library/pdb.html) in your code 
and need to interact with the running Django process when the breakpoint is reached 
you can run [`docker attach`](https://docs.docker.com/engine/reference/commandline/attach/):

- Python 2.7: `docker attach cfgov-refresh_python2_1`
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

This repository includes code for generating a "production-like" Docker Image. 

## How do I use it?

You can generate and run it locally via docker-compose with:

`docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build`

(This will create images running both Python 2.7 and 3.6, and also spin up containers for Postgres and Elasticsearch, much like the development 'compose' environment.)

If you just want to generate an image using , you can use:

`docker build . --build-arg scl_python_version=rh-python36 -t your-desired-image-name`

The 'scl_python_version' build argument refers to the the [Python Software Collection](https://www.softwarecollections.org/en/scls/?search=python) to use. We've tested this against `python27` and `rh-python36`.

Once you've generated the image, you'll probably want to [`docker push`](https://docs.docker.com/engine/reference/commandline/push/) it to the repository of your choice. From there, it should be deployable (with some configuration) on any platform that supports Docker images.

## What's inside?

The image includes:

- the `cfgov` django project, and all Python dependencies, built against the selected scl_python_version
- Apache, configured to run with the apache configuration included in cfgov-refresh, including a mod_wsgi version that matches scl_python_version.
- The results of running the cfgov-refresh front-end build (`./frontend.sh production`) and the django 'collectstatic' command.

## How does it work?

The production image *starts* with our development image. If you look at the Dockerfile, this is spelled out by the line:

`FROM cfgov-dev as cfgov-prod`

Both 'cfgov-dev' and 'cfgov-prod' are called "[build stages](https://docs.docker.com/develop/develop-images/multistage-build/)". That line means, "create a new stage, starting from cfgov-dev, called cfgov-prod".

From there, we:
- set a bunch of environment variables-
- install Apache, and the mod_wsgi version appropriate for our chosen `scl_python_version`
- *temporarily* install node and yarn
- run frontend.sh, Django's collectstatic command, and then *uninstall* node and yarn.
- clean up some unnecessary files, and create a few symbolic links
- Set the default command on container startup to `httpd -d ./cfgov/apache -D FOREGROUND`, which runs apache using the [configuration in cfgov-refresh](https://github.com/cfpb/cfgov-refresh/tree/master/cfgov/apache), in the foreground (instead of as a background service. This is typical when running Apache in a container).
