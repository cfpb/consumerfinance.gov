# Running in a Virtual Environment

First, follow
[the standalone installation instructions](../installation/#stand-alone-installation)
to create your virtual environment, install required dependencies, and run
the setup scripts.

You will generally have three tabs (or windows) open in your terminal,
which will be used for:

 1. **Git operations**.
    Perform Git operations and general development in the repository,
    such as `git checkout main`.
 2. **Elasticsearch**.
    Run an Elasticsearch (ES) instance.
    See instructions [below](#2-run-elasticsearch-optional).
 3. **Django server**. Start and stop the web server.
    Server is started with `./runserver.sh`,
    but see more details [below](#3-load-indexes--launch-site).

What follows are the specific steps for each of these tabs.

### 1. Git operations

From this tab you can do Git operations,
such as checking out our main branch:

```bash
git checkout main
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
`development` or `production`, which will affect how the build is made.
To install dependencies of one environment or the other run `./frontend.sh`
(dependencies and devDependencies) or `./frontend.sh production`
(dependencies but not devDependencies).

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
First, move into the `consumerfinance.gov` project directory
and ready your environment:

```bash
# Use the consumerfinance.gov virtualenv.
workon consumerfinance.gov

# cd into this directory (if you aren't already there)
cd consumerfinance.gov
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

### yarn commands
The following yarn tasks are available:

```
yarn scripts             # Build the Javascript with esbuild
yarn styles              # Build the Less with esbuild w/ its PostCSSPlugin
yarn copy                # Move static files to the output directory
yarn build               # Run scripts, styles, and copy along with app-specific scripts
yarn watch               # Run the build then watch JS and LESS changes
yarn lint                # Run frontend linting
yarn jest                # Run frontend tests
yarn test                # Run both
```

### Reinstalling the virtual environment

To remove an existing virtual environment for
[a reinstall of consumerfinance.gov](../installation/#stand-alone-installation),
first deactivate the virtual environment if it is active:

```bash
deactivate
```

Then remove the existing virtual environment:

```bash
rmvirtualenv consumerfinance.gov
```

After this, you may follow
[the installation instructions](installation/#stand-alone-installation)
again.
