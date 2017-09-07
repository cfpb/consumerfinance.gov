# cfgov-refresh

[![Build Status](https://travis-ci.org/cfpb/cfgov-refresh.png?branch=master)](https://travis-ci.org/cfpb/cfgov-refresh?branch=master)
[![Code Climate](https://codeclimate.com/github/cfpb/cfgov-refresh.png?branch=master)](https://codeclimate.com/github/cfpb/cfgov-refresh?branch=master)
[![codecov](https://codecov.io/gh/cfpb/cfgov-refresh/branch/master/graph/badge.svg)](https://codecov.io/gh/cfpb/cfgov-refresh)

The redesign of the [www.consumerfinance.gov](http://www.consumerfinance.gov) website.
This Django project includes the front-end assets and build tools,
[Jinja templates](http://jinja.pocoo.org) for front-end rendering,
and [Wagtail CMS](https://wagtail.io) for content administration.

![Screenshot of cfgov-refresh](homepage.png)


## Quickstart

Full [installation](https://cfpb.github.io/cfgov-refresh/installation/)
and [usage](https://cfpb.github.io/cfgov-refresh/usage/) instructions
are available in [our documentation](https://cfpb.github.io/cfgov-refresh).

Ensure that Elasticsearch and MySQL are installed and that MySQL is
either running or runnable by our
[backend.sh script](https://github.com/cfpb/cfgov-refresh/blob/master/backend.sh#L41)
and our
[runserver.sh script](https://github.com/cfpb/cfgov-refresh/blob/master/runserver.sh#L12).

```
git clone git@github.com:cfpb/cfgov-refresh.git
cd cfgov-refresh
pip install virtualenv virtualenvwrapper
npm install -g gulp
source load-env.sh
source setup.sh
./runserver.sh
```


## Documentation

Documentation for this project is available in the [docs](docs/) directory
and [online](https://cfpb.github.io/cfgov-refresh/).

If you would like to browse the documentation locally, you can do so
with `mkdocs`:

```
git clone git@github.com:cfpb/cfgov-refresh.git
cd cfgov-refresh
pip install virtualenv virtualenvwrapper
source activate-virtualenv.sh
pip install mkdocs
mkdocs serve
```


## Getting help

Use the [issue tracker](https://github.com/cfpb/cfgov-refresh/issues) to follow the
development conversation.
If you find a bug not listed in the issue tracker,
please [file a bug report](https://github.com/cfpb/cfgov-refresh/issues/new).


## Getting involved

We welcome your feedback and contributions.
See the [contribution guidelines](CONTRIBUTING.md) for more details.

Additionally, you may want to consider
[contributing to the Capital Framework](https://cfpb.github.io/capital-framework/contributing/),
which is the front-end pattern library used in this project.


## Open source licensing info
1. [TERMS](TERMS.md)
2. [LICENSE](LICENSE)
3. [CFPB Source Code Policy](https://github.com/cfpb/source-code-policy/)


## Credits and references

This project uses the [Capital Framework](https://github.com/cfpb/capital-framework)
for its user interface and layout components.
