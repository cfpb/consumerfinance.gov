# Installation and configuration for cfgov-refresh

## Clone the repository

Using the console, navigate to the root directory in which your projects live and clone this project's repository:

```bash
git clone git@github.com:cfpb/cfgov-refresh.git
cd cfgov-refresh
```

You may also wish to fork the repository on GitHub and clone the resultant personal fork. This is advised if you are going to be doing development on `cfgov-refresh` and contributing to the project.

There are two ways to install cfgov-refresh:

- [Stand-alone installation](#stand-alone-installation)
- [Docker-compose installation](#docker-compose-installation)


## Stand-alone installation

These instructions are somewhat specific to developing on Mac OS X,
but if you're familiar with other Unix-based systems,
it should be fairly easy to adapt them to your needs.

### Install system-level requirements

#### virtualenv & virtualenvwrapper Python modules

Install [virtualenv](https://virtualenv.pypa.io/en/latest/index.html)
and [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/)
to be able to create a local environment for your server:

```bash
pip install virtualenv virtualenvwrapper
```

#### Autoenv module

This project uses a large number of environment variables.

To automatically define environment variables and launch the virtualenv
upon `cd`ing to the project folder,
[install Autoenv](https://github.com/kennethreitz/autoenv#install).
We recommend using [Homebrew](http://brew.sh):

```bash
brew install autoenv
```

After installation, Homebrew will output instructions similar to:

```bash
To finish the installation, source activate.sh in your shell:
  source /Users/[YOUR USERNAME]/homebrew/opt/autoenv/activate.sh
```

Run that now for your initial setup.
Any time you run the project you’ll need to run that last line, so
if you’ll be working with the project consistently,
we suggest adding it to your Bash profile by running:

```bash
echo 'source /Users/[YOUR USERNAME]/homebrew/opt/autoenv/activate.sh' >> ~/.bash_profile
```

If you need to find this info again later, you can run:

```bash
brew info autoenv
```


!!! note
    If you use Zsh you’ll need to use
    [zsh-autoenv](https://github.com/Tarrasch/zsh-autoenv),
    but we can’t provide support for issues that may arise.

#### MySQL

If you're developing on OS X, this should be installed by default,
and you shouldn't have to do anything else to get it working.
You can optionally install a different version with Homebrew.

#### Elasticsearch

!!! warning
    __These instructions are deprecated since Elasticsearch 1.7
    is no longer supported by `brew`.__

[Install Elasticsearch 1.7](https://www.elastic.co/guide/en/elasticsearch/reference/1.7/setup.html)
however you’d like. We use [Homebrew](http://brew.sh) for developing on OS X):

```bash
brew tap homebrew/versions
brew search elasticsearch
brew install homebrew/versions/elasticsearch17
```

Just as with Autoenv, Homebrew will output similar instructions after installation:

```bash
# To have launchd start homebrew/versions/elasticsearch17 now and restart at login:
  brew services start homebrew/versions/elasticsearch17
# Or, if you don't want/need a background service you can just run:
  elasticsearch --config=/Users/[YOUR USERNAME]/homebrew/opt/elasticsearch17/config/elasticsearch.yml
```

Any time you resume work on the project after restarting your machine,
you’ll need to open a new tab and run that last line.
If you’ll be working on the project consistently,
we suggest using the first option, so you don't have to worry about that.
Note that some older versions of Homebrew may suggest
using `launchctl` instead of `brew services`.

If you need to find this info again later, you can run:

```bash
brew info elasticsearch17
```

#### Front-end dependencies

The cfgov-refresh front end currently uses the following frameworks / tools:

- [Gulp](http://gulpjs.com): task management for pulling in assets,
  linting and concatenating code, etc.
- [Less](http://lesscss.org): CSS pre-processor.
- [Capital Framework](https://cfpb.github.io/capital-framework/getting-started):
  User interface pattern-library produced by the CFPB.

!!! note
    If you’re new to Capital Framework, we encourage you to
    [start here](https://cfpb.github.io/capital-framework/getting-started).

1. Install [Node.js](http://nodejs.org) however you’d like.
   We recommend using [nvm](https://github.com/creationix/nvm), though.

2. Install [Gulp](http://gulpjs.com):

```bash
npm install -g gulp
```

!!! note
    This project requires Node.js v5.5 or higher, and npm v3 or higher.


#### Set up your environment

If this is the first time you're setting up the project, run the following
script to copy `.env_SAMPLE` to `.env`, export your environment variables,
and activate your virtualenv for the first time.

```bash
source load-env.sh
```

Each time you start a new session for working on this project, you'll need to
get those environment variables and get your virtualenv running again.
If you setup Autoenv earlier, this will happen for you automatically when you
`cd` into the project directory.

If you prefer not to use Autoenv, just be sure to `source .env` every time
you start a new session of work on the project.

#### Run the setup script

At this point, your machine should have everything it needs to automate the
rest of the setup process.

If you haven't cloned this repo yet, clone it to a local folder.
Because related projects will need to be installed as siblings to this project,
we recommend putting them all in their own folder, e.g., `~/Projects/cf.gov`.

Once cloned, from the project root (`~/Projects/cf.gov/cfgov-refresh/`),
run this command to complete the setup process:

```bash
source setup.sh
```

This will take several minutes, going through the steps in these scripts:

1. `frontend.sh`
1. `backend.sh`

Once complete, you should have a fully functioning local environment,
ready for you to develop against!

There are some [optional setup steps](#optional-steps)
that you may want to perform before continuing.

Want to know more about what the setup scripts are doing?
[Read the detailed rundown.](#curious-about-what-the-setup-scripts-are-doing)

Get any errors? [See our troubleshooting tips.](#troubleshooting)

**Continue following the [usage instructions](usage).**

## Docker-compose installation

### Tools we use for developing with Docker

- **Docker**: You may not need to interact directly with Docker: but you should know that it's a client/server application for managing "containers" (a way of running software in an isolated environment) and "images" (a snapshot of all of the files neccessary to run a container).
- **Docker Compose**: Compose allows you to configure and run a collection of connected containers (like a web application and it's database) 
- **Docker Machine**: Docker only runs natively on Linux and Windows. On OS X, we'll use Docker Machine to start the Docker server in a virtual linux environment (using Virtualbox)

#### Frontend note

We have not *yet* brought the front end build process into Docker, so you will still need to follow the "stand alone" guidence for [front-end dependencies](https://cfpb.github.io/cfgov-refresh/installation/#front-end-dependencies) and run `./frontend.sh` to build static assets.

### 1. Setup your Docker environment 

If you have never installed Docker before, follow the instructions [here](https://docs.docker.com/engine/installation/) or from your operating system vendor. If you are on a mac and are unable to install the official "Docker for Mac" package, the quickstart instructions below might help.

If you are on a machine that is already set up to run Linux docker containers, please install [Docker Compose](https://docs.docker.com/compose/install/). If `docker-compose ps` runs without error, you can can go to step 2. 

#### Mac + Homebrew + Virtualbox quickstart

**Starting assumptions**: You already have homebrew and virtualbox installed. You can run `brew search docker` without error.

1. Install Docker, Docker Machine, and Docker Compose: `brew install docker docker-compose docker-machine`
2. `source mac-virtualbox-init.sh`
 
At this point, `docker-compose ps` should run without error. 

### 2.  Run the site

The following assumes you have checked out cfgov-refresh, and have an open terminal, in the cfgov-refresh directory.

Our docker-compose.yml configuration expects there to be a .python_env file. You can create a blank one quickly with:

`touch .python_env`

However, you could save some time and effort later (if you have access to the CFPB network), by configuring a URL for database dumps. The complete .python_env file will look like this:

```
CFGOV_PROD_DB_LOCATION=https://(rest of the URL)
```

You can get that URL at [GHE]/CFGOV/platform/wiki/Database-downloads#resources-available-via-s3

From here you should be able to simply run:

`docker-compose up`

This will download and/or build images, and then start the containers, as described in the docker-compose.yml file. This will take a few minutes, or longer if you are on a slow internet connection.

When it's all done, you should be able to load http://localhost:8000 in your browser, and see a database error.

### 3.  Get a database

In a seperate terminal window or tab, run `eval $(docker-machine env)`. This will produce no output, but configures that terminal session so that docker-compose and docker will work.

Run `./shell.sh`. This opens a bash shell inside your Python container.

If you followed the suggestion above about setting CFGOV_PROD_DB_LOCATION in .python_env, you should be able to run:

`./refresh-data.sh`

Otherwise, [the standalone instructions](https://cfpb.github.io/cfgov-refresh/installation/#load-a-database-dump) should be enough to get you started.

Once you have a database loaded, you should have a functioning copy of site working at http://localhost:8000

### 4. Next Steps

#### Interacting with Docker Machine

If you used 'mac-virtualbox-init.sh', then we used Docker Machine to create a virtualbox VM, running the docker server. Here are some useful docker machine commands:

- Start and stop the VM with  `docker-machine start` and `docker-machine stop`
- get the current machine IP with `docker-machine ip`
- if for some reason you want to start over, `docker-machine rm default`, and `source mac-virtualbox-init.sh`

You'll need to run this command in any new terminal window or tab:

`eval $(docker-machine env)`

It may be helpful to run `docker-machine env` by itself, so you understand what's happening. Those variables are what allows docker-compose and the docker command line tool, running natively on your mac, to connect to the Docker server running inside virtualbox.

If you use autoenv (described in the stand-alone intructions) or something similar, you might consider adding `eval $(docker-machine env)` to your .env file. You could also achieve the same results (and start the VM if it's not running yet) with `source mac-virtualbox-init.sh`

Any further Docker documentation will assume you are either in a shell where you have already run `eval $(docker-machine env)`, or you are in an environment where that's not neccessary.

#### How do I...

See the Docker section of the [usage](../usage/) page.

## Optional steps

### Load initial data into database

The `initial-data.sh` script can be used to initialize a new database to make
it easy to get started working on Wagtail. This script first ensures that all
migrations are applied to the database, and then does the following:

- Creates an `admin` superuser with a password as specified in the
`WAGTAIL_ADMIN_PW` environment variable, if set.
- If it doesn't already exist, creates a new Wagtail home page named `CFGOV`,
with a slug of `cfgov`.
- Updates the default Wagtail site to use the port defined by the `DJANGO_HTTP_PORT` environment variable, if defined; otherwise this port is set to 80.
- If it doesn't already exist, creates a new [wagtail-sharing](https://github.com/cfpb/wagtail-sharing) `SharingSite` with a hostname and port defined by the `DJANGO_STAGING_HOSTNAME` and `DJANGO_HTTP_PORT` environment variables.

### Load a database dump

If you're installing this fresh, the initial data you receive will not be
as extensive as you'd probably like it to be.

You can get a database dump by:

1. Going to [GHE]/CFGOV/platform/wiki/Database-downloads
1. Selecting one of the extractions and downloading the `production_django.sql.gz` file
1. Unzip it
1. Run:

```bash
./refresh-data.sh /path/to/dump.sql
```

The `refresh-data.sh` script will apply the same changes as the `initial-data.sh` script described above (including setting up the `admin` superuser), but will not apply migrations.

To apply any unapplied migrations to a database created from a dump, run:

```bash
python cfgov/manage.py migrate
```

### Set variables for working with the GovDelivery API

Uncomment and set the GovDelivery environment variables in your `.env` file.

!!! note
    GovDelivery is a third-party web service that powers our emails.
    The API is used by subscribe forms on our website.
    Users may decide to swap this tool out for another third-party service.


## Curious about what the setup scripts are doing?

Here's a rundown of each of the scripts called by `setup.sh` and what they do.

### 1. `frontend.sh`

1. **Initialize project dependency directories** (`init`)

   This script first checks for an argument passed from the command line
   that can trigger different options for different environments.
   Since you ran it with no arguments, it will set up the dev environment.

   It then creates a checksum for `package-lock.json` (if it exists) and
   `package.json`.
   This will be used later to determine if dependencies need to be installed.

   It will then set some env vars for the Node dependency directories.
1. **Clean and install project dependencies** (`clean_and_install`)

   The script will now compare the checksums to see if it needs to install
   dependencies, or if they are already up-to-date.

   If the checksums do not match, the script will empty out all installed
   dependencies (`clean`) so the new installation can start fresh,
   then install the latest requested dependencies (`install`).

   The `devDependencies` from `package.json` are not installed
   if the environment is production, and if it's the dev or test environment,
   it checks to see if Protractor is globally installed.

   Finally, it creates a new checksum for future comparisons.
1. **Run tasks to build the project for distribution** (`build`)

   Finally, the script runs `gulp build` to rebuild the front-end assets.
   It no longer cleans first, because the gulp-changed plugin prevents
   rebuilding assets that haven't changed since the last build.

   If this is the production environment, it also triggers style and script
   builds for `ondemand` and `nemo`, which aren't part of a standard
   `gulp build`.

### 2. `backend.sh`

1. **Confirm environment** (`init`)

   This script first checks for an argument passed from the command line
   that can trigger different options for different environments.
   Since you ran it with no arguments, it will set up the dev environment.

   It will then run a script to ensure that you're in a virtualenv.
   If not, the script will end, to prevent you from accidentally installing
   your Python dependencies globally.
1. **Install project dependencies** (`install`)

   Python dependencies are installed into the virtualenv via pip.
   Dependencies vary slightly depending on whether we're in dev, test, or prod.
1. **Setup MySQL server** (`db_setup`)

   Finally, the script will start the MySQL server, if it's not already running,
   run `create-mysql-db.sh` to create the database using
   the variables given in `.env`, if it's not already there,
   and will run `initial-data.sh` to create the first Wagtail user
   and load some basic initial data.


## Troubleshooting

Here are some common issues and how you can fix them:

### Errors referencing South, or other Python errors:

Since moving to Django 1.8, we use Django's built-in migration engine,
and we no longer use South.
If you're getting South errors, you probably have it installed globally.
To solve this, from outside the virtual environment, run `pip uninstall south`.

If you're getting other kinds of Python errors (for example, when running tox),
you may even want to go as far as uninstalling all globally-installed
Python packages: `pip freeze | grep -v "^-e" | xargs pip uninstall -y`.
After doing that, you'll need to reinstall virtualenv:
`pip install virtualenv virtualenvwrapper`.
