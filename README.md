# consumerfinance.gov

This is a fork of the [main cfgov-refresh](https://github.com/cfpb/cfgov-refresh) for [Raft's](https://goraft.tech/) work on the Digital Money Toolkit project. Some of the User Research, Design, and Technical artifacts can be found [in the Wiki](https://github.com/raft-tech/cfgov-refresh/wiki). The ReactJS codebase is integrated into Wagtail Django CMS as a satellite application.

[![Build Status](https://github.com/cfpb/consumerfinance.gov/workflows/test/badge.svg?branch=master)](https://github.com/cfpb/consumerfinance.gov/actions)

## Backlog

The backlog for this project is being maintained in the CFPB Enterprise GitHub whereas the bugs are captured in this fork. 

## Pull request process

We follow the following steps for developing and creating end-of-sprint pull-request reviews:

1. Raft developers create PR's from their branches into `my-money-calendar`
2. The PR is reviewed and issues are resolved as new commits to the same branch
3. The PR is merged after the manual review and the tests via CircleCI pass
4. A new PR is open from `my-money-calendar` to `cfgov-refres/my-money-calendar`
5. The PR follows the [pull request template](https://github.com/raft-tech/cfgov-refresh/blob/master/.github/PULL_REQUEST_TEMPLATE.md)
6. The PR is reviewed/merged and deployed to CFPB dev servers 
7. When functionality is ensured, a PR is opened from `cfgov-refres/my-money-calendar` to `cfgov-refres/master`


## Quickstart

Full installation and usage instructions are available in
[our documentation](https://cfpb.github.io/consumerfinance.gov).

This project requires Python 3.6, Node 12, and Gulp 4.
We recommend the use of [virtualenv](https://virtualenv.pypa.io/en/stable/) and
[virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
for keeping the project's Python dependencies contained.

Clone the repository:

```sh
git clone git@github.com:cfpb/consumerfinance.gov.git
```

Create a virtual environment for Python dependencies:

```sh
cd consumerfinance.gov
mkvirtualenv --python=python3.6 consumerfinance.gov
```

Create and load initial environment settings:

```sh
cp -a .env_SAMPLE .env
source .env
```

Install third-party dependencies and build frontend assets:

```sh
./setup.sh
```

Create a local database, a Wagtail admin user, and a site homepage:

```sh
./initial-data.sh
```

Start your local Django server:

```sh
./runserver.sh
```

Your site will be available locally at <http://localhost:8000/>.

The Wagtail admin area will be available at <http://localhost:8000/admin/>,
which you can log into with the credentials `admin`/`admin`.


## Documentation

Full documentation for this project is available in the [docs/](docs/) directory
and [online](https://cfpb.github.io/consumerfinance.gov/).

If you would like to browse the documentation locally, you can do so
with [`mkdocs`](https://www.mkdocs.org/):

```sh
pip install -r requirements/docs.txt
mkdocs serve
```

Documentation will be available locally at
[http://localhost:8000/](http://localhost:8000/).


## Getting help

Use the [issue tracker](https://github.com/cfpb/consumerfinance.gov/issues)
to follow the development conversation.
If you find a bug not listed in the issue tracker,
please [file a bug report](https://github.com/cfpb/consumerfinance.gov/issues/new).


## Getting involved

We welcome your feedback and contributions.
See the [contribution guidelines](CONTRIBUTING.md) for more details.

Additionally, you may want to consider
[contributing to the Design System](https://cfpb.github.io/design-system/#help-us-make-improvements),
which is the front-end pattern library used in this project.


## Open source licensing info

1. [TERMS](TERMS.md)
2. [LICENSE](LICENSE)
3. [CFPB Source Code Policy](https://github.com/cfpb/source-code-policy/)


## Credits and references

This project uses [Design System](https://github.com/cfpb/design-system)
as the basis of its user interface and layout components.
