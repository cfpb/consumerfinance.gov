## Usage: Stand Alone

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

## Usage: Docker

Much of the guidance above for the "stand-alone" set-up still stands, and it
is worth reviewing in full. Here are some things that might be different:

- `docker-compose` takes care of running Elasticsearch for you, and all
Elasticsearch, Postgres, and Python output will be shown in a single Terminal
window or tab. (wherever you run `docker-compose up`)
- `manage.py` commands can only be run after you've opened up a terminal in the
Python container, which you can do with `./shell.sh`
- There is not *yet* a good way to use SSL/HTTPS, but that is in the works
- You won't ever need to use `backend.sh` or `runserver.sh`

### How do I...

#### Use Docker Machine

If you used `mac-virtualbox-init.sh`, then we used Docker Machine to create a
VirtualBox VM, running the Docker server. Here are some useful `docker-machine`
commands:

- Start and stop the VM with  `docker-machine start` and `docker-machine stop`
- get the current machine IP with `docker-machine ip`
- if for some reason you want to start over, `docker-machine rm default`, and
  `source mac-virtualbox-init.sh`

To enable Docker and Docker Compose commands, you'll always first need to run
this command in any new shell:

`eval $(docker-machine env)`

It may be helpful to run `docker-machine env` by itself, so you understand
what's happening. Those variables are what allows `docker-compose` and the
`docker` command line tool, running natively on your Mac, to connect to the
Docker server running inside VirtualBox.

If you use autoenv (described in the stand-alone intructions) or something
similar, you might consider adding `eval $(docker-machine env)` to your .env
file. You could also achieve the same results (and start the VM if it's not
running yet) with `source mac-virtualbox-init.sh`

Any further Docker documentation will assume you are either in a shell where
you have already run `eval $(docker-machine env)`, or you are in an environment
where that's not neccessary.

#### Run manage.py commands like migrate, shell, and dbshell, and shell scripts like refresh-data.sh

run `./shell.sh` to open up a shell *inside* the Python container. From there,
commands like `cfgov/manage.py migrate` should run as expected.

The same goes for scripts like `./refresh-data.sh` and `./initial-data.sh` –
they will work as expected once you're inside the container.

In addition you can run single commands by passing them as arguments to
`shell.sh`, for example:

`./shell.sh cfgov/manage.py migrate`

#### Use PDB

Run `./attach.sh` to connect to the TTY session where `manage.py runserver` is
running. If the app is paused at a PDB prompt, this is where you can access it.

#### Handle updates to Python requirements

If Compose is running, stop it with CTRL-C. Run:

`docker-compose build python`

This will update your Python image. The next time you run `docker-compose up`,
the new requirements will be in place.

#### Set environment variables

Environment variables from your `.env` file are sourced when the python container
starts and when you access a running container with `./shell.sh` Your shell
environment variables, however, are not visible to applications running in Docker.
To add new environment variables, simply add them to the `.env` file, stop compose
with ctrl-c, and start it again with `docker-compose up`.

#### Get familiar with Docker Compose, and our configuration

docker-compose.yml contains a sort of "recipe" for running the site. Each entry
in the Compose file describes a component of our application stack (Postgres,
Elasticsearch, and Python), and either points to a public image on Dockerhub,
or to a Dockerfile in cfgov-refresh. You can learn a lot more about Compose
files in [the docs](https://docs.docker.com/compose/compose-file/)

Similarly, a Dockerfile contains instructions for transforming some base image,
to one that suits our needs. The Dockerfile sitting in the top level of
cfgov-refresh is probably the most interesting. It starts with
[the public CentOS:7 image](https://hub.docker.com/_/centos/), and installs
everything else neccessary to run our Python dependencies and the Django app
itself.  This file will only be executed:

- the first time you run `docker-compose up` (or the first time after you
re-create the Docker Machine VM)
- any time you run `docker-compose build`

That's why you need to run `docker-compose build` after any changes to
/requirements/

There are other compose subcommands you might be interested in. Consider
[learning about](https://docs.docker.com/compose/reference/overview/)
`build`, `restarts`, `logs`, `ps`, `top`, and the `-d` option for `up`.

#### Develop satellite apps

Check out any apps you are developing into the develop-apps directory. These
will automatically be added to the
[PYTHONPATH](https://docs.python.org/2/using/cmdline.html#envvar-PYTHONPATH),
and apps contained within will be importable from Python running in the
container.

For example, if your app is called 'foobar', in a repo called foobar-project,
you could clone foobar-project in to develop apps:

`git clone https://github.com/myorg/foobar-project`

... which will create a directory at develop-apps/foobar-project. Assuming
'foobar' is at the top-level of 'foobar-project', you should be able to
import it from your python code:

```python
import foobar
```
#### runserver has crashed! How do I start it again

In a separate terminal window or tab, running `docker-compose up python` should
restart the server.
