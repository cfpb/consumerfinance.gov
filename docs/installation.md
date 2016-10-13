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
- [Vagrant-box installation](#vagrant-box-installation)

!!! danger
    The instruction for Vagrant are not currently working.

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


## Vagrant-box installation

!!! danger
	These instructions are not currently working, but we'd like to get them working soon. [PRs welcome](contributing).

### 1. Environment variables setup

The project uses a number of environment variables.
The `setup.sh` script will create a `.env` file for you
from the `.env_SAMPLE` file found in the repository,
if you don't already have one.

Inside the `.env` file you can customize the project environment configuration.

If you would like to manually copy the environment settings,
copy the `.env_SAMPLE` file and un-comment each variable after
adding your own values.
```bash
cp -a .env_SAMPLE .env && open -t .env
```

Then load the environment variables with:
```bash
. ./.env
```

### 2. Fetch extra playbooks

The project pulls together various open source and closed source plays. The plays are
managed through ansible-galaxy, a core module for this exact purpose. To download all
the dependencies, use this command:

```bash
ansible-galaxy install -r ansible/requirements.yml
```

### 3. Launch Vagrant virtual environment

The project uses Vagrant to create the simulated virtual environment allowing the developer
to work on a production-like environment while maintaining development work on the
local machine. To create this virtual environment, you need to execute the following command.

```bash
vagrant up
```

!!! note
	Please be patient the first time you run this step.

### 4. Front-end Tools

In order to run the application, we must generate the front-end assets.
After running the following commands, visit http://localhost:8001 to see the site running.
You can also place the first two export commands into your `.bashrc` to simplify things later.

```bash
export CFGOV_HOME=path/to/cfgov-refresh
export PATH=$PATH:$CFGOV_HOME/bin
cfgov init
cfgov assets
cfgov start django
```


## Optional steps

### Load initial data into database

The `initial-data.sh` script can be used to initialize a new database to make
it easy to get started working on Wagtail. This script first ensures that all
migrations are applied to the database, and then does the following:

- Creates an `admin` superuser with a password as specified in the
`WAGTAIL_ADMIN_PW` environment variable, if set.
- If it doesn't already exist, creates a new Wagtail home page named `CFGOV`,
with a slug of `cfgov`.
- If it doesn't already exist, creates a new Wagtail Site with a hostname of
`content.localhost`, with the root page set to the `CFGOV` home page.
- If they don't already exist, creates pages for events (name `Events`, slug
`events`) and archived events (name `Archive`, slug `archive`).

### Load a database dump from the Build server

If you're installing this fresh, the initial data you receive will not be
as extensive as you'd probably like it to be.

You can get a database dump using the `cf.gov-dump-rdbms`
Jenkins job. Download the `sql.gz` file,
unzip it, and then run:

```bash
./refresh-data.sh /path/to/dump.sql
```

This will remove the initial Wagtail admin user that was created by
the `initial-data.sh` script that was called by `backend.sh`.
If you need to access the Wagtail admin, create a new user with the following:

```
./cfgov/manage.py createsuperuser
```

### Install Protractor locally

Protractor (for the test suites) can be installed globally
to avoid downloading Chromedriver repeatedly.
To do so, run:

```bash
npm install -g protractor && webdriver-manager update
```

### Install dependencies for working with the GovDelivery API

Install the following GovDelivery dependencies into your virtual environment:

```bash
pip install git+git://github.com/dpford/flask-govdelivery
pip install git+git://github.com/rosskarchner/govdelivery
```

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

   It will then set some env vars for the Node and Bower dependency directories.
1. **Clean project dependencies** (`clean`)

   The script will now empty out all installed dependencies,
   so the new installation can start fresh.
1. **Install project dependencies** (`install`)

   Node and Bower dependencies are installed.
   The `devDependencies` from `package.json` are not installed
   if the environment is production, and if it's the dev or test environment,
   it checks to see if Protractor is globally installed.
1. **Run tasks to build the project for distribution** (`build`)

   Finally, the script executes `gulp clean` to wipe out any lingering
   `dist` files, then runs `gulp build` to rebuild everything.

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
