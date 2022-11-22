# consumerfinance.gov

The primary repository for [consumerfinance.gov](https://www.consumerfinance.gov/).
This Django project includes the front-end assets and build tools,
[Jinja templates](https://jinja.palletsprojects.com/) for front-end rendering,
code to configure our CMS, [Wagtail](https://wagtail.io/),
and several standalone Django apps for specific parts of the site.

## Documentation

Full documentation for this project is available in the [docs/](docs/) directory
and [online](https://cfpb.github.io/consumerfinance.gov/).

## Quickstart

This quickstart requires a working Docker Desktop installation and git:

- [Clone the repository](https://cfpb.github.io/consumerfinance.gov/installation/#clone-the-repository):

  ```shell
  git clone https://github.com/cfpb/consumerfinance.gov.git
  cd consumerfinance.gov
  ```

- One of the following runtimes:

  - [Set up and run the Docker containers via docker-compose](https://cfpb.github.io/consumerfinance.gov/installation/#set-up-and-run-the-docker-containers):

    ```shell
    docker-compose up
    ```

  - [Set up and run the Docker containers via Kubernetes via Helm](https://cfpb.github.io/consumerfinance.gov/installation/#set-up-and-run-the-docker-containers):

    ```shell
    ./build-images.sh && ./helm-install.sh
    ```

  if you see an error like:

  ```
  Error: Kubernetes cluster unreachable: Get "http://localhost:8080/version": dial tcp [::1]:8080: connect: connection refused
  ```

  then you need to activate Kubernetes in your docker desktop settings!

  This may take some time, as it will also
  [load initial data](https://cfpb.github.io/consumerfinance.gov/installation/#load-initial-data)
  and
  [build the frontend](https://cfpb.github.io/consumerfinance.gov/installation/#build-the-frontend).

consumerfinance.gov should now be available at <http://localhost:8000>.

Our documentation will be available at <http://localhost:8888> (docker-compose only).

The Wagtail admin area will be available at <http://localhost:8000/admin/>,
which you can log into with the credentials `admin`/`admin`.

## Getting the package

Packages are tagged into one of three groups: main Branch -> latest, PRs -> pr-#, and Release -> major.minor.patch. The github SHA of the commit packaged should be listed as a label.
To see our Docker image packages you can vist [Packages page](https://github.com/cfpb/consumerfinance.gov/pkgs/container/consumerfinance.gov)

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
