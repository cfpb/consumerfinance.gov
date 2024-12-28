# Deploying to RHEL/CentOS servers

This repository includes code for generating a self-extracting zip archive
of the code and all of its Python dependencies. We use these
archives to deploy the site to a Linux server.

## Generating an artifact

We use a custom CentOS 7-based Docker image (`cfgov-artifact-builder`) to build
deployment artifacts.
CentOS is used so that the Python modules that include compiled code will
be compiled for the same environment in which they will be run.

This image is updated automatically via GitHub Actions and stored in the
GitHub Container registry.

To download the image from GitHub (after first
[authenticating](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#authenticating-to-the-container-registry)):

```sh
docker pull ghcr.io/cfpb/cfgov-artifact-builder:latest
```

Alternatively, to build the image locally:

```sh
docker build docker/centos7 --target=cfgov-artifact-builder -t ghcr.io/cfpb/cfgov-artifact-builder:latest
```

To use the image to build a deployable artifact from your local source code:

```sh
docker run -v `pwd`:/cfgov ghcr.io/cfpb/cfgov-artifact-builder:latest
```

The generated artifact will be created in the current directory as
`cfgov_current_build.zip`.

Note that artifacts generated locally may include extra files from local development
directories that are not intended to be deployed to production.
Only artifacts generated in a clean environment (e.g. on GitHub Actions)
should be used in real deployments.

## What's in an artifact?

A deployable artifact is a zipfile that can be executed by Python.
It contains the full project source code and static assets
along with various additional files.

A `__main__.py` file contains [the code that runs when the zip file is invoked
as a Python module](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/deployable_zipfile/extract.py).

A `wheels/` directory contains all of our python dependencies, while
`bootstrap_wheels/` contains modules needed at deployment time, to install
everything.

`loadenv.py` and `loadenv-init.pth` are used to load environment variables from
a `environment.json` file, deployed seperately.

Before the final version of the zip file is saved, we prepend a python "shebang"
line, `#!/usr/bin/env python`.
This, combined with `__main__.py` described above, is what makes the file
executable and self-extracting.

## Deploying an artifact

We currently use Ansible to prepare servers to run an artifact, and to do the actual deployment.
If we ignore some specifics and quirks of our environment, the basic steps look something like this:

1. copy the artifact to the system
2. execute the artifact, with the -d (destination) argument, `./artifact.zip -d destination-dir`. This
   will unpack the files, create a new virtualenv, and install all of the wheels in `wheels/` into that
   virtualenv. **Important Note:** This should be done with the same Python interpreter that will run the
   application. For example, on our servers this means using [`scl enable`](https://linux.die.net/man/1/scl)
   to specify a particular Python version from
   [Software Collections](https://www.softwarecollections.org/en/scls/?search=python).
3. put an `environment.json` file in place, in your `destination-dir`
4. run Django utilities like 'collectstatic' and 'migrate'
5. update a symlink to point to the latest release
6. restart your WSGI server.

## Testing an artifact

A CentOS-based Docker image (`cfgov-artifact-tester`) can be used to test deployable artifacts locally without requiring access to a Linux server.
This image unpacks a deployable artifact and runs it in a Docker container in the
same way it runs on RHEL/CentOS servers.

This image is updated automatically via GitHub Actions and stored in the
GitHub Container registry.

To download the image from GitHub (after first
[authenticating](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#authenticating-to-the-container-registry)):

```sh
docker pull ghcr.io/cfpb/cfgov-artifact-tester:latest
```

Alternatively, to build the image locally:

```sh
docker build docker/centos7 --target=cfgov-artifact-tester -t ghcr.io/cfpb/cfgov-artifact-tester:latest
```

To use the image to test a local deployable artifact named `cfgov_current_build.zip`:

```sh
docker run -it -v `pwd`:/cfgov:ro -p 8000:80 --env-file docker/centos7/test.env cfgov-artifact-tester:latest
```

Running this container extracts the local artifact and serves it using an Apache
webserver accessible locally at http://localhost:8000.

The `docker/centos7/test.env` file includes various environment variables that can
be modified to alter the application's behavior.
