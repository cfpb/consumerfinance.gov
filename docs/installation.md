# Setting up consumerfinance.gov

## Quickstart

This quickstart requires a working Docker Desktop installation and git:

- [Clone the repository](#clone-the-repository):

    ```sh
    git clone https://github.com/cfpb/consumerfinance.gov.git
    cd consumerfinance.gov
    ```

- [Set up and run the Docker containers](#set-up-and-run-the-docker-containers):

    ```sh
    docker-compose up
    ```

    This may take some time, as it will also
    [load initial data](#load-initial-data)
    and
    [build the frontend](#build-the-frontend).

consumerfinance.gov should now be available at <http://localhost:8000>.

This documentation will be available at <http://localhost:8888>.

The Wagtail admin area will be available at <http://localhost:8000/admin/>,
which you can log into with the credentials `admin`/`admin`.

Please see
our [running consumerfinance.gov](/running/) documentation
for next steps.

There are also optional steps described below, as well as
[alternative setup options](#alternative-setups).

## Detailed installation

The [quickstart above](#quickstart) should get you started.
Each step has some additional detail below.

### Clone the repository

Using the console, navigate to the root directory in which your projects
live and clone this project's repository:

```sh
git clone git@github.com:cfpb/consumerfinance.gov.git
cd consumerfinance.gov
```

Configure `.git-blame-ignore-revs` by running the following command within
the repository:

```sh
git config blame.ignoreRevsFile .git-blame-ignore-revs
```

### Set up the environment (optional)

The consumerfinance.gov Django site relies on environment variables defined
in a `.env` file. If this is your first time setting up the project,
copy `.env_SAMPLE` to `.env`:

```sh
cp -a .env_SAMPLE .env
```

### Set up a local Python environment (optional)

For running our
[Python unit tests, linting, etc](/python-unit-tests/)
outside of the Docker container, we rely on a local Python environment.

!!! note
    Our local Python environment requires [pyenv](https://github.com/pyenv/pyenv)
    with
    [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv).
    They can be installed from Homebrew on macOS:

    ```sh
    brew install pyenv pyenv-virtualenv
    ```

    Python 3.8 must then be installed once pyenv is installed:

    ```sh
    pyenv install 3.8.12
    ```

First we need to create a Python virtualenv for consumerfinance.gov:

```sh
pyenv virtualenv 3.8.12 consumerfinance.gov
```

Then we'll need to activate it.
Activating the virtualenv is necessary before using it in the future as well:

```sh
pyenv activate consumerfinance.gov
```

Once activated, our Python CI requirements can be installed in the virtualenv:

```sh
pip install -r requirements/ci.txt
```

### Install pre-commit
We use `pre-commit` to automatically run our linting tools before a commit 
takes place. These tools consist of `black`, `flake8`, and `isort`. To install 
`pre-commit`, running the following commands from within the 
`consumerfinance.gov` directory:

```sh
pip install -U pre-commit && pre-commit install
```

Before each commit, `pre-commit` will execute and run our `pre-commit` checks.
If any task fails, it will attempt to resolve the issue automatically, notify 
you of the changes (if any), and ask for you to re-stage the changed files. If 
all checks pass, a commit will take place as expected, allowing you to then 
push to GitHub. This is to reduce the number of commits with failed lints, and
to assist developers with linting without thinking.


### Install our private fonts (optional)

consumerfinance.gov uses a proprietary licensed font, Avenir.

If you want to pull this from a content delivery network (CDN),
you can set the
[`@use-font-cdn`](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/unprocessed/css/main.less#L30)
to `true` and rebuild the assets with `yarn gulp build`.

If you want to install self-hosted fonts locally, you can place the font files
in `static.in/cfgov-fonts/fonts/`.

If you are a CFPB employee, you can perform this step with:

```
git clone https://[GHE]/CFGOV/cfgov-fonts/ static.in/cfgov-fonts
```

Where `[GHE]` is our GitHub Enterprise URL.

### Build the frontend

!!! note
    Our frontend requires [Node.js 16](https://nodejs.org/en/)
    with
    [Yarn](https://yarnpkg.com/).
    We prefer
    [nvm](https://github.com/nvm-sh/nvm)
    for Node.js version management.
    nvm can be installed using:

    ```sh
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | sh
    ```

    Node 16 must then be installed once nvm is installed:

    ```sh
    nvm install 16
    ```

    Node.js 16 can then be used in any sh using:

    ```sh
    nvm use 16
    ```

    Yarn must then be installed:

    ```sh
    curl -o- -L https://yarnpkg.com/install.sh | sh
    ```

We have a single script that will install our frontend dependencies for both
building and
[unit testing/linting/etc](/javascript-unit-tests/):

```sh
./frontend.sh
```

Gulp can be used to rebuild our assets after the initial setup:

```sh
yarn gulp build
```

!!! note
    If you are having trouble loading JavaScript edits locally, you may need to turn off service workers for localhost:8000. Learn how to [manage service workers in Firefox and Chrome](https://love2dev.com/blog/how-to-uninstall-a-service-worker/).

### Set up and run the Docker containers

consumerfinance.gov depends on PostgreSQL database and Elasticsearch.
We use
[`docker-compose`](https://docs.docker.com/compose/)
to run these services along side the consumerfinance.gov Django site.

To build and run our Docker containers for the first time, run:

```sh
docker-compose up
```

This will build and start our PostgreSQL, Elasticsearch, Python, and
documentation services.

The first time this is fun, it will
[load initial data](#load-initial-data)
and
[build the frontend](#build-the-frontend)
for you.

### Load initial data

Our `initial-data.sh` script can be used to initialize a new database to make
it easy to get started working on consumerfinance.gov.
This script ensures that all migrations are applied to the database
and then does the following:

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

This script must be run inside the Docker `python` container:

```sh
docker-compose exec python bash
./initial-data.sh
```

### Load a database dump

Alternatively, one of our database dumps can be installed using our
`refresh-data.sh` script. You can get a database dump by defining
`CFGOV_PROD_DB_LOCATION` in your `.env` file as described in
GitHub Enterprise at
[GHE]/CFGOV/platform/wiki/Database-downloads#resources-available-via-s3, or
inside a Docker `python` container sh immediately before running
`refresh-data.sh`:

```sh
docker-compose exec python bash
CFGOV_PROD_DB_LOCATION=http://(rest of the URL)
./refresh-data.sh
```

`refresh-data.sh` can also be given a path to a gziped database dump:

```sh
./refresh-data.sh /path/to/dump.sql.gz
```

This automatically [(re)builds the Elasticsearch index](/search/#building-the-index),
unless you run the `refresh-data.sh` script with the `--noindex` flag.


## Alternative setups

consumerfinance.gov requires a Python environment, PostgreSQL, and
Elasticsearch to run. None of this requires Docker, Docker is simply a
convenient way to ensure consistent versioning and running of these services
along with the consumerfinance.gov Django site.

The consumerfinance.gov Django site can be run locally in a virtualenv and can
use PostgreSQL and Elasticsearch from either
our [`docker-compose`](https://docs.docker.com/compose/) file
or from Homebrew.

### PostgreSQL and Elasticsearch from Docker

To build and start only
the PostgreSQL (`postgres`)
and Elasticsearch (`elasticsearch`)
containers from our
[`docker-compose`](https://docs.docker.com/compose/) file,
explicitly specify them as arguments to `docker-compose`:

```
docker-compose up postgres elasticsearch
```

This will expose
PostgreSQL on port `5432` on `localhost`
and
Elasticsearch on port `9200` on `localhost`.

### PostgreSQL and Elasticsearch from Homebrew

You can install PostgreSQL and Elasticsearch from Homebrew if you're on a Mac:

```sh
brew install postgresql
brew install elasticsearch
```

Once it's installed, you can configure it to run as a service:

```sh
brew services start postgresql
brew services start elasticsearch
```

Our recommended Postgres configuration is a database named `cfgov` and a user
named `cfpb`, with data stored in schema `cfpb`. This can be created with the
following commands:

```sh
dropdb --if-exists cfgov && dropuser --if-exists cfpb
psql postgres -c "CREATE USER cfpb WITH LOGIN PASSWORD 'cfpb' CREATEDB"
psql postgres -c "CREATE DATABASE cfgov OWNER cfpb"
psql postgres://cfpb:cfpb@localhost/cfgov -c "CREATE SCHEMA cfpb"
```

We don't support using an SQLite database because we use database fields
that are specific to Postgres. The `CREATEDB` keyword above allows the
`cfpb` user to create a temporary Django database when running unit tests.

### Set up the `consumerfinance.gov` virtualenv

After you have chosen a means to run PostgreSQL and Elasticsearch,
[set up the environment](#set-up-the-environment),
[set up a local Python environment](#set-up-a-local-python-environment),
optionally [installed our private fonts](#install-our-private-fonts),
and [built the frontend](#build-the-frontend),
all the Python dependencies for running locally can be installed:

```sh
pyenv activate consumerfinance.gov
pip install -r requirements/local.txt
```

Once complete, our `runserver.sh` script will bring up the site at
[http://localhost:8000](http://localhost:8000).

```sh
./runserver.sh
```

## Additional setup

### Sync local image and document storage (optional)

If using a database dump, pages will contain links to images or documents
that exist in the database but don't exist on your local disk.
This will cause broken or missing images or links when browsing the site locally.

This is because in production images and documents are stored on S3,
but when running locally they are stored on disk.

This project includes two Django management commands that can be used to download
any remote images or documents referenced in the database so that they can be served when
running locally.

This command downloads all remote images (and image renditions) referenced in the
database, retrieving them from the specified URL and storing them in the
specified local directory:

```sh
cfgov/manage.py sync_image_storage https://files.consumerfinance.gov/f/ ./cfgov/f/
```

This command does the same, but for documents:

```sh
cfgov/manage.py sync_document_storage https://files.consumerfinance.gov/f/ ./cfgov/f/
```

### Install GNU gettext for Django translation support (optional)

In order to generate Django translations as documented
[here](translation.md), you'll need to install the
[GNU gettext](https://www.gnu.org/software/gettext/) library.

On macOS, GNU gettext is available via Homebrew:

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
