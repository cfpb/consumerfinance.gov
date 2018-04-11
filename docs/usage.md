## Usage: Stand Alone

If not using the Vagrant box, you will generally have four tabs
(or windows) open in your terminal, which will be used for:

 1. **Git operations**.
    Perform Git operations and general development in the repository,
    such as `git checkout master`.
 2. **Elasticsearch**.
    Run an Elasticsearch (ES) instance.
    See instructions [below](#2-run-elasticsearch).
 3. **Django server**. Start and stop the web server.
    Server is started with `./runserver.sh`,
    but see more details [below](#3-load-indexes--launch-site).
 4. **Gulp watch**.
    Run the Gulp watch (`gulp watch`) task to automatically re-run the gulp
    asset compilation tasks when their source files are changed.

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

### 2. Run Elasticsearch

!!! note
	This Elasticsearch tab (or window) might not be necessary if you opted for the `launchd` option when [installing Elasticsearch](installation#elasticsearch).

To launch Elasticsearch, first find out where your Elasticsearch config file is located.
You can do this with [Homebrew](https://brew.sh) using:

```bash
brew info elasticsearch
```

The last line of that output should be the command you need to launch Elasticsearch with the
proper path to its configuration file. For example, it may look like:

```bash
elasticsearch --config=/Users/[YOUR MAC OSX USERNAME]/homebrew/opt/elasticsearch/config/elasticsearch.yml
```

### 3. Load Indexes & Launch Site
First, move into the `cfgov-refresh` project directory
and ready your environment:

```bash
# Use the cfgov-refresh virtualenv.
workon cfgov-refresh

# cd into this directory (if you aren't already there)
cd cfgov-refresh
```

Index the latest content from the API output from a WordPress and Django back-end.
**This requires the constants in [Stand alone installation](installation#stand-alone-installation) to be set.**

```bash
python cfgov/manage.py sheer_index -r
```

!!! note
	To view the indexed content you can use a tool called
	[elasticsearch-head](https://mobz.github.io/elasticsearch-head/).

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

To set up a superuser in order to access the Wagtail admin:

```
python cfgov/manage.py createsuperuser
```

To view the site browse to: <http://localhost:8000>

!!! note "Using a different port"
	If you want to run the server at a port other than 8000 use

    `python cfgov/manage.py runserver <port number>`

    Specify an alternate port number, e.g. `8001`.

To view the Wagtail admin login,
browse to: <http://localhost:8000/admin/login/>

!!! note "Using HTTPS locally"
    To access a local server using HTTPS use

    `./runserver.sh ssl`

    You'll need to ignore any browser certificate errors.

### 4. Launch the Gulp watch task

To watch for changes in the source code and automatically update the running site,
open a terminal and run:

``` bash
gulp build
gulp watch
```

!!! note
    The watch task will only re-run the tasks that have changed files.
    Also, you must run `gulp build` at least once before watching.

!!! warning "Server error"
    If you get this message on the page when running `gulp watch`:
    "A server error occurred.  Please contact the administrator."
    You likely need to delete files with the `.pyc` extension from the project with the following command:    
    `find . -name \"*.pyc\" -delete`

#### Available Gulp Tasks
In addition to `gulp watch`, there are a number of other important gulp tasks,
particularly `gulp build` and `gulp test`,
which will build the project and test it, respectively.
Using the `gulp --tasks` command you can view all available tasks.
The important ones are listed below:

```
gulp build           # Concatenate, optimize, and copy source files to the production /dist/ directory.
gulp clean           # Remove the contents of the production /dist/ directory.
gulp lint            # Lint the scripts and build files.
gulp docs            # Generate JSDocs from the scripts.
gulp test            # Run linting, unit and acceptance tests (see below).
gulp test:unit       # Run only unit tests on source code.
gulp test:acceptance # Run only acceptance (in-browser) tests on production code.
gulp watch           # Watch for source code changes and auto-update a browser instance.
```

## Usage: Docker

Much of the guidance above for the "stand-alone" set-up still stands, and it
is worth reviewing in full. Here are some things that might be different:

- `docker-compose` takes care of running Elasticsearch for you, and all
Elastisearch, MySQL, and Python output will be shown in a single Terminal
window or tab. (whereever you run `docker-compose up`)
- `manage.py`commands can only be run after you've opened up a terminal in the
Python container, which you can do with `./shell.sh`
- There is not *yet* a good way to use SSL/HTTPS, but that is in the works
- You won't ever use these scripts: `setup.sh`, `backend.sh`, `runserver.sh`

### How do I...

#### Use Docker Machine

If you used `mac-virtualbox-init.sh` or `setup.sh docker`, then we used Docker
Machine to create a virtualbox VM, running the docker server. Here are some
useful docker machine commands:

- Start and stop the VM with  `docker-machine start` and `docker-machine stop`
- get the current machine IP with `docker-machine ip`
- if for some reason you want to start over, `docker-machine rm default`, and
  `source mac-virtualbox-init.sh`

You'll need to run this command in any new terminal window or tab:

`eval $(docker-machine env)`

It may be helpful to run `docker-machine env` by itself, so you understand
what's happening. Those variables are what allows docker-compose and the docker
command line tool, running natively on your mac, to connect to the Docker
server running inside virtualbox.

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

The same goes for scripts like `./refresh-data.sh` and `./initial-data.sh` --
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

Your shell environment variables (and the variables in your .env file, if you
are using one) are not visible to applications running in Docker. If you need
to set variables that will be visible to Django, and in `./shell.sh`, you'll
need to set them in the .python_env file, and restart the python container (it
might be simpler to simple stop compose with ctrl-c, and start it again with
`docker-compose up`)

.python_env is *not* a shell script, like your .env file, ~/.bash_profile, etc.
See the [Docker Compose docs](https://docs.docker.com/compose/compose-file/#env_file)

#### Get familiar with Docker Compose, and our configuration

docker-compose.yml contains a sort of "recipe" for running the site. Each entry
in the Compose file describes a component of our application stack (MySQL,
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

In a seperate terminal window or tab, `docker-compose up python` should restart
it.
