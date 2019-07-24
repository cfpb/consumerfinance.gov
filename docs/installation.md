# Installation and configuration for cfgov-refresh

## Clone the repository

Using the console, navigate to the root directory in which your projects
live and clone this project's repository:

```bash
git clone git@github.com:cfpb/cfgov-refresh.git
cd cfgov-refresh
```

You may also wish to fork the repository on GitHub and clone the resultant
personal fork. This is advised if you are going to be doing development on
`cfgov-refresh` and contributing to the project.

There are two ways to install cfgov-refresh:

- [Stand-alone installation](#stand-alone-installation)
- [Docker-compose installation](#docker-compose-installation)


## Stand-alone installation

These instructions are somewhat specific to developing on macOS,
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
We recommend using [Homebrew](https://brew.sh):

```bash
brew install autoenv
```

After installation, Homebrew will output instructions similar to:

```bash
To finish the installation, source activate.sh in your shell:
  source /Users/[YOUR USERNAME]/homebrew/opt/autoenv/activate.sh
```

Run that now for your initial setup.
Any time you run the project you’ll need to run that last line,
so if you’ll be working with the project consistently,
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

#### Front-end dependencies

The cfgov-refresh front-end build process currently
includes the following frameworks / tools:

- [Gulp](https://gulpjs.com): task management for pulling in assets,
  linting and concatenating code, etc.
- [Less](http://lesscss.org): CSS pre-processor.
- [Capital Framework](https://cfpb.github.io/capital-framework/getting-started):
  User interface pattern-library produced by the CFPB.
- [Node.js](https://nodejs.org). Install however you’d like.
  We recommend using [nvm](https://github.com/creationix/nvm), though.
  If your node version is outdated you should receive a console error to upgrade
  while attempting to build the project.
- [Yarn](https://yarnpkg.com).
  We recommend installing using [Homebrew](https://brew.sh):

```bash
# Use --ignore-dependencies to use your system installed node version
brew install yarn --ignore-dependencies
```


#### Webfonts

The site uses a proprietary licensed font, Avenir.
If you want to pull this from a content delivery network (CDN),
you can set the
[`@use-font-cdn`](https://github.com/cfpb/cfgov-refresh/blob/master/cfgov/unprocessed/css/main.less#L30)
to `true` and rebuild the assets with `yarn run gulp build`.
If you want to install self-hosted fonts locally, you can place the font files
in `static.in/cfgov-fonts/fonts/` and restart the local web server.
If you are a CFPB employee, you can perform this step with:

```
cd static.in/ && git clone https://[GHE]/CFGOV/cfgov-fonts/
```
Where `[GHE]` is our GitHub Enterprise URL.

#### Set up your environment

The Django app relies on environment variables defined in a `.env` file. If this
is your first time setting up the project, copy `.env_SAMPLE` to `.env` and then
`source` that file:

```bash
cp -a .env_SAMPLE .env
source .env
```

Each time you start a new session for working on this project, you'll need to
get those environment variables and get your virtualenv running again.

If you setup Autoenv earlier, this will happen for you automatically when you
`cd` into the project directory.

If you prefer not to use Autoenv, just be sure to `source .env` every time
you start a new session of work on the project.

#### Install Postgres

If you're on a Mac and use Homebrew, you can easily install Postgres:

```bash
brew install postgresql
```

Once it's installed, you can configure it to run as a service:

```bash
brew services start postgresql
```

Then create the database, associated user, and schema for that user:

```bash
dropdb --if-exists cfgov && dropuser --if-exists cfpb
createuser cfpb && createdb -O cfpb cfgov
psql postgres://cfpb@localhost/cfgov -c 'CREATE SCHEMA cfpb'
```

If you absolutely need to use SQLite, you'll need to update your `.env` file
to comment out the line that specifies Postgres as the db:

```bash
# export DATABASE_URL=postgres://cfpb@localhost/cfgov
```

And then uncomment the line that tells Django to use SQLite:

```bash
export DATABASE_URL=sqlite:///db.sqlite3
```

#### Run the setup script

At this point, your machine should have everything it needs to automate the
rest of the setup process.

If you haven't cloned this repo yet, clone it to a local folder.
Because related projects will need to be installed as siblings to this project,
we recommend putting them all in their own folder, e.g., `~/Projects/cf.gov`.

Once cloned, from the project root (`~/Projects/cf.gov/cfgov-refresh/`),
run this command to complete the setup process:

```bash
./setup.sh
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

**Continue following the [usage instructions](../running-virtualenv/).**

## Docker-compose installation

### Tools we use for developing with Docker

- **Docker**: You may not need to interact directly with Docker, but you
  should know that it's a client/server application for managing _containers_
  (a way of running software in an isolated environment) and _images_ (a
  snapshot of all of the files neccessary to run a container).
- **Docker Compose**: Compose allows you to configure and run a collection of
  connected containers (like a web application and its database).
- **Docker Machine**: In environments where Docker Engine is not available,
  Docker Machine can be used to create and manage Docker hosts on virtual
  machines.

### 1. Setup your Docker environment

If you have never installed Docker before, follow the instructions
[here](https://docs.docker.com/engine/installation/) or from your operating
system vendor. If you are on a mac and are unable to install the official
"Docker for Mac" package, the quickstart instructions below might help.

If you are on a machine that is already set up to run Linux docker containers,
please install [Docker Compose](https://docs.docker.com/compose/install/).
If `docker-compose ps` runs without error, you can can go to step 2.

#### Copy the `.env_SAMPLE` file over

The Docker Compose setup (see `docker-compose.yml`) provides the environment
variables defined in `.env` to the container running the Django app. If
this is your first time setting up the project, copy `.env_SAMPLE` to
`.env`:

```bash
cp -a .env_SAMPLE .env
```

#### Mac + Homebrew + Docker Machine + VirtualBox quickstart

**Starting assumptions**: You already have Homebrew and VirtualBox installed.
You can run `brew search docker` without error.

Install Docker, Docker Machine, and Docker Compose:
`brew install docker docker-compose docker-machine`

Then run `source mac-virtualbox-init.sh` to initialize your Docker Machine
setup.

At this point, `docker-compose ps` should run without error.

### 2. Setup your frontend environment

Refer to the [front-end dependencies](#front-end-dependencies) described above
in the [standalone installation instructions](#stand-alone-installation).

### 3. Run setup

`./setup.sh docker`

This will install and build the frontend and set up the docker environment.

### 4. Run Docker Compose for the first time

`docker-compose up`

This will download and/or build images, and then start the containers, as
described in the docker-compose.yml file. This will take a few minutes, or
longer if you are on a slow internet connection.

When it's all done, you should be able to load http://localhost:8000 in your
browser, and see a database error.

### 3. Setup the database

Run `./shell.sh`. This opens a bash shell inside your Python container.

You can either [load initial data](#load-initial-data-into-database) per the
instructions below, or load a database dump.

You could save some time and effort later (if you have access to the CFPB
network), by configuring a URL for database dumps in the `.env` file.

```
CFGOV_PROD_DB_LOCATION=http://(rest of the URL)
```

You can get that URL at
[GHE]/CFGOV/platform/wiki/Database-downloads#resources-available-via-s3

With `CFGOV_PROD_DB_LOCATION` in `.env` you should be able to run:

`./refresh-data.sh`

Otherwise, [the instructions to load a database dump](#load-a-database-dump)
below should be enough to get you started.

Once you have a database loaded, you should have a functioning copy of site
working at [http://localhost:8000](http://localhost:8000)

### 4. Next Steps

See [Running in Docker](../running-docker/) to continue after that.

## Optional steps

### Load initial data into database

The `initial-data.sh` script can be used to initialize a new database to make
it easy to get started working on Wagtail. This script first ensures that all
migrations are applied to the database, and then does the following:

- Creates an `admin` superuser with password `admin`.
- If it doesn't already exist, creates a new Wagtail home page named `CFGOV`,
with a slug of `cfgov`.
- Updates the default Wagtail site to use the port defined by the
`DJANGO_HTTP_PORT` environment variable, if defined; otherwise this port is
set to 80.
- If it doesn't already exist, creates a new
[wagtail-sharing](https://github.com/cfpb/wagtail-sharing) `SharingSite` with
a hostname and port defined by the `WAGTAIL_SHARING_HOSTNAME` and
`DJANGO_HTTP_PORT` environment variables.

### Load a database dump

If you're installing this fresh, the initial data you receive will not be
as extensive as you'd probably like it to be.

You can get a database dump by:

1. Going to [GHE]/CFGOV/platform/wiki/Database-downloads
1. Selecting one of the extractions and downloading the
   `production_django.sql.gz` file
1. Run:

```bash
./refresh-data.sh /path/to/dump.sql.gz
```

The `refresh-data.sh` script will apply the same changes as the
`initial-data.sh` script described above (including setting up the `admin`
superuser), but will not apply migrations.

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

### Install GNU gettext for Django translation support

In order to generate Django translations as documented
[here](translation.md), you'll need to install the
[GNU gettext](https://www.gnu.org/software/gettext/) library.

On MacOS, GNU gettext is available via Homebrew:

```
brew install gettext
```

but it gets installed as
["keg-only"](https://docs.brew.sh/FAQ#what-does-keg-only-mean) due to conflicts
with the default installation of BSD gettext. This means that GNU gettext won't
be loaded in your PATH by default. To fix this, you can run

```
brew link --force gettext
```

to force its installation, or see `brew info gettext` for an alternate
solution.

If installed locally, you should be able to run this command successfully:

```
$ gettext --version
```

GNU gettext is also required to run our translation-related unit tests locally.

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

   Finally, the script runs `yarn run gulp build` to rebuild the front-end assets.
   It no longer cleans first, because the gulp-changed plugin prevents
   rebuilding assets that haven't changed since the last build.

   If this is the production environment, it also triggers style and script
   builds for `ondemand` and `nemo`, which aren't part of a standard
   `gulp build`.

!!! note
    If you are having trouble loading JavaScript edits locally, you may need to turn off service workers for localhost:8000. Learn how to [manage service workers in Firefox and Chrome](https://www.ghacks.net/2016/03/02/manage-service-workers-in-firefox-and-chrome/).


### 2. `backend.sh`

!!! note
    `backend.sh` is not used for our Docker setup.

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
