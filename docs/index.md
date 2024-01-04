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

- `deployment.in`: requirements to run consumerfinance.gov in any environment
- `test.in`: requirements for executing Python tests locally or in CI
- `dev.in`: requirements for development work, running, and testing
- `docs.in`: requirements to build the consumerfinance.gov docs
- `scripts.in`: Requirements for running our smoke test and alert polling scripts without having to install all the other requirements
