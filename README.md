# consumerfinance.gov

The primary repository for [consumerfinance.gov](https://www.consumerfinance.gov/).
This Django project includes the front-end assets and build tools,
[Jinja templates](https://jinja.palletsprojects.com/) for front-end rendering,
code to configure our CMS, [Wagtail](https://wagtail.io/),
and several standalone Django apps for specific parts of the site.

## Quickstart

Full installation and usage instructions are available in
[our documentation](https://cfpb.github.io/consumerfinance.gov).

This quickstart requires a working Docker Desktop installation and git:

- [Clone the repository](https://cfpb.github.io/consumerfinance.gov/installation/#clone-the-repository):

    ```shell
    git clone https://github.com/cfpb/consumerfinance.gov.git
    cd consumerfinance.gov
    ```

- [Set up and run the Docker containers](https://cfpb.github.io/consumerfinance.gov/installation/#set-up-and-run-the-docker-containers):

    ```shell
    docker-compose up
    ```

    This may take some time, as it will also
    [load initial data](https://cfpb.github.io/consumerfinance.gov/installation/#load-initial-data)
    and
    [build the frontend](https://cfpb.github.io/consumerfinance.gov/installation/#build-the-frontend).

consumerfinance.gov should now be available at <http://localhost:8000>.

Our documentation will be available at <http://localhost:8888>.

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
