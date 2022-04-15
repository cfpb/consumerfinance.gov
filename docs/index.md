# Introduction to consumerfinance.gov

This is the documentation for the consumerfinance.gov project that powers the [www.consumerfinance.gov](https://www.consumerfinance.gov) website. It is organized thematically in order to create a central repository for all information pertaining to consumerfinance.gov.

## Disclaimer

**This project is a work in progress.** Nothing presented in this repo—whether in the source code, issue tracker, or wiki—is a final product unless it is marked as such or appears on [www.consumerfinance.gov](https://www.consumerfinance.gov). In-progress updates may appear on [beta.consumerfinance.gov](https://beta.consumerfinance.gov).

## Technology stack

The standard technology stack for development of consumerfinance.gov within the CFPB consists of the following base:

- macOS
- [Homebrew](https://brew.sh) - package manager for installing system software on OSX
- [Python 3.8](https://docs.python.org/3.8/) and [pip (Python package manager)](https://pip.pypa.io/en/stable/user_guide/)
- [Jinja2 templates](https://jinja.palletsprojects.com/) for front-end rendering. See [`requirements/libraries.txt`](https://github.com/cfpb/consumerfinance.gov/tree/main/requirements/libraries.txt) for version.
- [Wagtail CMS](https://wagtail.io) for content administration. See [`requirements/wagtail.txt`](https://github.com/cfpb/consumerfinance.gov/tree/main/requirements/wagtail.txt) for version.
- [PostgreSQL 10.5](https://www.postgresql.org/) is the database we use in production and locally.
- [Psycopg](http://initd.org/psycopg/) is the Python library that lets Python talk to Postgres. See [`requirements/libraries.txt`](https://github.com/cfpb/consumerfinance.gov/tree/main/requirements/libraries.txt) for current version.
- Additional dependencies, listed below.

## Additional dependencies

- [Elasticsearch](https://www.elastic.co):
  Used for full-text search capabilities and content indexing.
- [Node](http://nodejs.org) and [yarn](https://yarnpkg.com/):
  Used for downloading and managing front-end dependencies and assets. Front-end dependencies are listed in the project's [package.json](https://github.com/cfpb/consumerfinance.gov/blob/main/package.json) file.
- [pyenv](https://github.com/pyenv/pyenv)
- [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)

## Versions

Versions for most front-end packages are kept updated in the project's [package.json](https://github.com/cfpb/consumerfinance.gov/blob/main/package.json) file.

Versions for back-end software including Django, Wagtail, Jinja, etc. are kept in the project's requirements files:
https://github.com/cfpb/consumerfinance.gov/tree/main/requirements

- `base.txt`: shortcut for `django.txt` + `wagtail.txt` + `libraries.txt`
- `ci.txt`: specific requirements for the continuous integration environment. Should/could be moved to CI configuration files?
- `deployment.txt`: requirements for deployment, includes `base.txt` and a New Relic library that we don't install anywhere else.
- `django.txt`: specifies the Django version. The file is used when running the site, but by having it separate we can test against other versions of Django by excluding this file.
- `docs.txt`: requirements to build the consumerfinance.gov docs.
- `libraries.txt`: Python libraries.
- `local.txt`: includes `base.txt` and some useful libraries when developing locally.
- `scripts.txt`: Requirements for running certain jobs on Jenkins, so scripts can run in Jenkins without having to install all the other requirements.
- `test.txt`: requirements for running Python tests.
- `wagtail.txt`: specifies Wagtail version. In its own file to make it easier to test multiple versions, same as with `django.txt`.
