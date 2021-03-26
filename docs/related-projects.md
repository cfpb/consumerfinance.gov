# Related Projects

## Satellite apps

We use the term "satellite apps" to refer to other CFPB-maintained Python
source code repositories and packages that provide functionality or content
for https://www.consumerfinance.gov but are not included in consumerfinance.gov.
Most but not all of these repositories can be run or tested without needing to
set up the full website.

We have six satellite apps that are maintained outside of the consumerfinance.gov codebase:

- [ccdb5-api](https://github.com/cfpb/ccdb5-api)
- [ccdb5-ui](https://github.com/cfpb/ccdb5-ui)
- [django-college-costs-comparison](https://github.com/cfpb/django-college-costs-comparison)
- [owning-a-home-api](https://github.com/cfpb/owning-a-home-api)
- [retirement](https://github.com/cfpb/retirement)
- [teachers-digital-platform](https://github.com/cfpb/teachers-digital-platform)

These satellite apps are imported into consumerfinance.gov as part of the project
[requirements files](https://github.com/cfpb/consumerfinance.gov/blob/main/requirements/libraries.txt).

!!! note "Thinking about making a new satellite app?"
    Satellite apps were originally built to be imported into the
    consumerfinance.gov website before we started using Wagtail to manage site
    content. We now prefer to build projects as apps inside the consumerfinance.gov
    repo. For more info, refer to the "Setting up new project code for
    consumerfinance.gov" page on the CFGOV/platform wiki on GHE.

## Other Python packages

CFPB also develops and maintains several other Python source code repositories
and packages that are used on https://www.consumerfinance.gov but are more
general-purpose.

These include:

- [django-flags](https://github.com/cfpb/django-flags)
- [wagtail-flags](https://github.com/cfpb/wagtail-flags/)
- [wagtail-inventory](https://github.com/cfpb/wagtail-inventory/)
- [wagtail-sharing](https://github.com/cfpb/wagtail-sharing)
- [wagtail-treemodeladmin](https://github.com/cfpb/wagtail-treemodeladmin)

The [cfpb/development](https://github.com/cfpb/development/) repository
contains the CFPB development guidelines used on these projects.

## Developing Python packages with consumerfinance.gov

Developers working on changes to satellite apps or other Python packages often
want or need to test their work as part of the larger consumerfinance.gov project.

The standard [installation](../installation/) process for consumerfinance.gov
includes whatever versions of these packages are specified in project 
[requirements files](https://github.com/cfpb/consumerfinance.gov/blob/main/requirements/libraries.txt).
Developers may want to temporarily or permanently replace those with a local
copy of package source code.

### Using a local virtual environment

When running in a virtual environment local to your developer machine,
standard usage of [`pip install`](https://docs.python.org/3/installing/index.html)
can be used to swap out package versions.

Running `pip install -e path/to/local/repo` will install local source code in
["editable"](https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs)
mode, replacing the satellite app version installed from requirements files
with your local copy:

```sh
# In a local virtual environment, after installing consumerfinance.gov.
# Python packages have been installed from requirements files.
# This includes, for example, the retirement satellite app:
(consumerfinance.gov) $ pip freeze | grep retirement
retirement==0.10.0

# Replace this version with an editable install pointing to your local copy.
(consumerfinance.gov) $ pip install -e ../retirement/
...
Installing collected packages: retirement
  Found existing installation: retirement 0.10.0
    Uninstalling retirement-0.10.0:
      Successfully uninstalled retirement-0.10.0
  Running setup.py develop for retirement
Successfully installed retirement

# The Python environment is now using the local copy.
(consumerfinance.gov) $ pip freeze | grep retirement
-e git+git@github.com:myfork/retirement.git@7d2b8eca86ed33d90b5cd7782e1f90b7ac89f6f9#egg=retirement
```

Installing a local copy of source code in editable mode ensures that any
changes made to files there will take effect immediately.

To switch back to the default version of a Python package, removing the use
of a local copy, you can manually install the version specified in the
requirements files:

```sh
(consumerfinance.gov) $ pip install retirement==0.10.0
```

Re-running the full virtual environment
[setup script](../installation/#run-the-setup-script)
will do the same thing.

### Using Docker

Working on Python packages requires a different approach when running
consumerfinance.gov locally with [its Docker setup](../running-docker/).
This is because while your local `consumerfinance.gov` directory is exposed to the
container, sibling directories or other locations where you might clone
other repositories are not.

For this reason, the Docker setup provides the ability to use the local
[`consumerfinance.gov/develop-apps`](https://github.com/cfpb/consumerfinance.gov/tree/main/develop-apps)
subdirectory as place to put local copies of Python packages.

Any packages put there (e.g. via a `git clone` of a satellite apps' repo)
will be automatically added to the
[PYTHONPATH](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH) 
in the Python containers.
Apps located within will be importable from Python running in the Docker
containers, and will take precedence over any versions installed from
requirements files as part of the Docker images.

To switch back to the default version of a Python package, removing the use
of a local copy, simply delete the copy from the `develop-apps` directory.

For any satellite apps that provide front-end assets that need to be built, 
you will need to run that step seperately:

```bash
# Check out the retirement satellite app into develop-apps:
cd develop-apps
git clone git@github.com:cfpb/retirement.git

# Build the front-end:
cd retirement
./frontendbuild.sh
```

If the satellite app needs any Python requirements that are not specified in 
[the consumerfinance.gov requirements](https://github.com/cfpb/consumerfinance.gov/tree/main/requirements/), 
they will need to be installed seperately by accessing the Python container shell
and using `pip`:

```bash
docker-compose exec python bash
pip install [PACKAGE NAME]
```
