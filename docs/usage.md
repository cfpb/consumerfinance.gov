## Usage

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
You can do this with [Homebrew](http://brew.sh) using:

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
	[elasticsearch-head](http://mobz.github.io/elasticsearch-head/).

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
