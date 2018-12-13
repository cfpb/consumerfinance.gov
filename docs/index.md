# Introduction

This is the documentation for the `cfgov-refresh` project, a redesign of the [www.consumerfinance.gov](https://www.consumerfinance.gov) website. It is organized thematically in order to create a central repository for all information pertaining to cfgov-refresh.

# Disclaimer

**This project is a work in progress.** Nothing presented in this repo—whether in the source code, issue tracker, or wiki—is a final product unless it is marked as such or appears on [www.consumerfinance.gov](https://www.consumerfinance.gov). In-progress updates may appear on [beta.consumerfinance.gov](https://beta.consumerfinance.gov).

# Technology stack

The standard technology stack for development of cfgov-refresh within the CFPB consists of the following base:

- macOS
- [Homebrew](https://brew.sh) - package manager for installing system software on OSX
- Python 2.7 and PIP (Python package manager)
- [Jinja2 templates](http://jinja.pocoo.org/docs/2.10/) for front-end rendering. Exact version is defined in [`requirements/libraries.txt`](https://github.com/cfpb/cfgov-refresh/tree/master/requirements/libraries.txt)
- [Wagtail CMS](https://wagtail.io) for content administration
- Additional dependencies, listed below

# Additional dependencies

- [Elasticsearch](https://www.elastic.co):
  Used for full-text search capabilities and content indexing.
- [Node 8](http://nodejs.org) and [yarn](https://yarnpkg.com/):
  Used for downloading and managing front-end dependencies and assets. Front-end dependencies are listed in the project's [package.json](https://github.com/cfpb/cfgov-refresh/blob/master/package.json) file.
- [Gulp 4](https://gulpjs.com/)
- [virtualenv](https://virtualenv.pypa.io/en/stable/)
- [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)

# Versions

Versions for most front-end packages are kept updated in the project's [package.json](https://github.com/cfpb/cfgov-refresh/blob/master/package.json) file.

Versions for back-end software including Python, etc are kept in the project's requirements files:
https://github.com/cfpb/cfgov-refresh/tree/master/requirements

- `base.txt`: shortcut for `django.txt` + `wagtail.txt` + `libraries.txt`
- `deployment.txt`: requirements for deployment, includes `base.txt` and `postgres.txt` and a New Relic library which we don't install anywhere else.
- `django.txt`: specifies Django version. In its own file to make it easier to test multiple versions. The file is used when running the site, but by having it separate we can test against other versions of Django by excluding this file.
- `libraries.txt`: Python libraries.
- `local.txt`: includes `base.txt` and `postgres.txt` and some useful libraries when developing locally.
- `docs.txt`: requirements to build the cfgov-refresh docs. 
- `optional-public.txt`: cfgov-refresh satellite apps. Should/could be moved into `libraries.txt`.
- `postgres.txt`: requirements to connect Django to Postgres.
- `scripts.txt`: Requirements for running certain jobs on Jenkins, so scripts can run in Jenkins without having to install all the other requirements. Maybe we shouldn't do this?
- `test.txt`: requirements for running Python tests.
- `travis.txt`: extra requirements for Travis. Should/could be moved to explicitly listed in the .travis.yml file?
- `wagtail.txt`: specifies Wagtail version. In its own file to make it easier to test multiple versions, same as with `django.txt`.