# Usage

- [Standalone](#standalone)
    1. [Git operations](#1-git-operations)
        - [Updating all dependencies](#updating-all-dependencies)
        - [Setting environments](#setting-environments)
    2. [Run Elasticsearch (optional)](#2-run-elasticsearch-optional)
    3. [Launch site](#3-launch-site)
        - [Available Gulp Tasks](#available-gulp-tasks)
- [Docker](#docker)
    - [Environment variables](#environment-variables)
    - [Access a container's shell](#access-a-containers-shell)
    - [Run Django management commands](#run-django-management-commands)
    - [Update Python dependencies](#update-python-dependencies)
    - [Work on satellite apps](#work-on-satellite-apps)
    - [Attach for debugging](#attach-for-debugging)
    - [Useful Docker commands](#useful-docker-commands)

## Standalone

You will generally have three tabs (or windows) open in your terminal,
which will be used for:

 1. **Git operations**.
    Perform Git operations and general development in the repository,
    such as `git checkout master`.
 2. **Elasticsearch**.
    Run an Elasticsearch (ES) instance.
    See instructions [below](#2-run-elasticsearch-optional).
 3. **Django server**. Start and stop the web server.
    Server is started with `./runserver.sh`,
    but see more details [below](#3-load-indexes--launch-site).

What follows are the specific steps for each of these tabs.

### 1. Git operations

From this tab you can do Git operations,
such as checking out our master branch:

```bash
git checkout master
```

#### Updating all dependencies

Each time you fetch from the upstream repository (this repo), run `./setup.sh`.
This setup script will remove and reinstall the project dependencies
and rebuild the site's JavaScript and CSS assets.

!!! note
    You may also run `./backend.sh` or `./frontend.sh`
    if you only want to re-build the backend or front-end, respectively.

##### Setting environments

The `NODE_ENV` environment variable can be set in your `.env` file to either
`development` or `production`, which will affect how the build is made and what
gulp tasks are available. To install dependencies of one environment
or the other run `./frontend.sh` (dependencies and devDependencies)
or `./frontend.sh production` (dependencies but not devDependencies).

### 2. Run Elasticsearch (optional)

Elasticsearch is needed for certain pieces of this project but is not a
requirement for basic functionality.

If Elasticsearch is installed via [Homebrew](https://brew.sh), you can see
instructions for running manually or as a background service using:

```bash
brew info elasticsearch
```

Typically to run Elasticsearch as a background service you can run:

```bash
brew services start elasticsearch
```

### 3. Launch Site
First, move into the `cfgov-refresh` project directory
and ready your environment:

```bash
# Use the cfgov-refresh virtualenv.
workon cfgov-refresh

# cd into this directory (if you aren't already there)
cd cfgov-refresh
```

From the project root, start the Django server:

```bash
./runserver.sh
```

!!! note
    If prompted to migrate database changes,
    stop the server with `ctrl` + `c` and run these commands:

```bash
python cfgov/manage.py migrate
./initial-data.sh
./runserver.sh
```

To view the site browse to: <http://localhost:8000>

!!! note "Using a different port"
    If you want to run the server at a port other than 8000 use

    `python cfgov/manage.py runserver <port number>`

    Specify an alternate port number, e.g. `8001`.

To view the Wagtail admin login,
browse to <http://localhost:8000/admin> and login with username `admin`
and password `admin` (created in `initial-data.sh` above; note that this
password will expire after 60 days).

!!! note "Using HTTPS locally"
    To access a local server using HTTPS use

    `./runserver.sh ssl`

    You'll need to ignore any browser certificate errors.

#### Available Gulp Tasks
There are a number of important gulp tasks,
particularly `build` and `test`,
which will build the project and test it, respectively.
Tasks are invoked via an `yarn run` command so that the local gulp-cli can be used.
Using the `yarn run gulp -- --tasks` command you can view all available tasks.
The important ones are listed below:

```
yarn run gulp build           # Concatenate, optimize, and copy source files to the production /dist/ directory.
yarn run gulp clean           # Remove the contents of the production /dist/ directory.
yarn run gulp lint            # Lint the scripts and build files.
yarn run gulp docs            # Generate JSDocs from the scripts.
yarn run gulp test            # Run linting, unit and acceptance tests (see below).
yarn run gulp test:unit       # Run only unit tests on source code.
yarn run gulp test:acceptance # Run only acceptance (in-browser) tests on production code.
yarn run gulp audit           # Run code quality audits.
```

## Docker

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
