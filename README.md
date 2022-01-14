# consumerfinance.gov

The primary repository for [consumerfinance.gov](https://www.consumerfinance.gov/).
This Django project includes the front-end assets and build tools,
[Jinja templates](https://jinja.palletsprojects.com/) for front-end rendering,
code to configure our CMS, [Wagtail](https://wagtail.io/),
and several standalone Django apps for specific parts of the site.

## Quickstart

Full installation and usage instructions are available in
[our documentation](https://cfpb.github.io/consumerfinance.gov).

This project requires Python 3.8, Node 16, and Gulp 4.
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
mkvirtualenv --python=python3.8 consumerfinance.gov
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
