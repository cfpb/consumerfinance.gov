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

- Python 2.7: `docker exec -it cfgov-refresh_python2_1 bash`
- Python 3.6: `docker exec -it cfgov-refresh_python3_1 bash`
- Elasticsearch: `docker exec -it cfgov-refresh_elasticsearch_1 bash`
- PostgreSQL: `docker exec -it cfgov-refresh_postgres_1 bash`

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

- Python 2.7: `docker-compose build python2`
- Python 3.6: `docker-compose build python3`

The next time you run `docker-compose up` the new requirements will be in place.

### Work on satellite apps

If you need to work on any of our 
[satellite apps](/satellite-repos/), 
you will need to perform a `git clone` in the 
[`develop-apps` directory](https://github.com/cfpb/cfgov-refresh/tree/master/develop-apps).
These will automatically be added to the
[PYTHONPATH](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH) 
in the Python containers, 
and apps contained within will be importable from Python running in the containers. 

For any satellite apps that provide front-end assets that need to be built, 
you will need to run that step seperately. 
For example, to work on [college-costs](https://github.com/cfpb/college-costs):

```bash
# Check out into develop-apps:
cd develop-apps
git clone https://github.com/cfpb/college-costs

# Build the front-end:
cd college-costs
./setup.sh
```

If the satellite app needs any Python requirements that are not specified in 
[the cfgov-refresh requirements](https://github.com/cfpb/cfgov-refresh/tree/master/requirements/), 
they will need to be installed seperately by 
[access the Python containers' shell](#access-the-containers-shell) 
and using `pip`:

Python 2.7: 

```bash
docker exec -it cfgov-refresh_python2_1 bash
pip2.7 install [PACKAGE NAME]
```

Python 3.6: 

```bash
docker exec -it cfgov-refresh_python3_1 bash
pip3.6 install [package name]
```


### Attach for debugging

If you have inserted a [PDB breakpoint](https://docs.python.org/3/library/pdb.html) in your code 
and need to interact with the running Django process when the breakpoint is reached 
you can run [`docker attach`](https://docs.docker.com/engine/reference/commandline/attach/):

- Python 2.7: `docker attach cfgov-refresh_python2_1`
- Python 3.6: `docker attach cfgov-refresh_python3_1`

When you're done, you can detach with `Ctrl+P Ctrl+Q`.


### Useful Docker commands

For `docker-compose` commands, 
`[CONTAINER]` is the container name that is defined in `docker-compose.yml`. 

For `docker` commands, `[CONTAINER]` is the container name displayed with `docker ps`.

- [`docker ps`](https://docs.docker.com/engine/reference/commandline/ps/)
    will list all containers.
- [`docker logs [CONTAINER]`](https://docs.docker.com/engine/reference/commandline/logs/)
    will print the logs of a container.
- [`docker top [CONTAINER]`](https://docs.docker.com/engine/reference/commandline/top/)
    will display the running processes in a container.
- [`docker-compose build [CONTAINER]`](https://docs.docker.com/compose/reference/build/)
    will build any of our configured containers.
