This repository includes code for generating a self-extracting zip archive
of the code and all of its Python dependencies. We use these
archives to deploy the site to a Linux server.

# Generating a deployment artifact

Running the script at `./docker/deployable-zipfile/build.sh` will start a CentOS 6
container, generate the artifact (via
[this script](https://github.com/cfpb/consumerfinance.gov/blob/main/docker/deployable-zipfile/_build.sh)),
and save it to `./cfgov_current_build.zip`.

We use CentOS 6 here, so that the Python modules that include compiled code, will
be compiled for the same environment they will be run in.

# What's in an artifact?

Here's a (very abbreviated) peek into what's *in* the zip file:

```
__main__.py
cfgov.pth
install_wheels.py
loadenv.py
loadenv-init.pth
wheels/botocore-1.10.84-py2.py3-none-any.whl
wheels/tqdm-4.15.0-py2.py3-none-any.whl
...
static.in/0/
static.in/0/fonts/
static.in/0/fonts/8344e877-560d-44d4-82eb-9822766676f9.woff
...
bootstrap_wheels/setuptools-41.2.0-py2.py3-none-any.whl
bootstrap_wheels/pip-19.2.3-py2.py3-none-any.whl
cfgov/...
```

The `__main__.py` file contains [the code that runs when the zip file is invoked
as a Python module](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/deployable_zipfile/extract.py).

The `wheels/` directory contains all of our python dependencies, while
`bootstrap_wheels/` contains modules needed at deployment time, to install
everything.

`loadenv.py` and `loadenv-init.pth` are used to load environment variables from
a `environment.json` file, deployed seperately.

Before the final version of the zip file is saved, we prepend a python "shebang" line,
`#!/usr/bin/env python`. This, combined with `__main__.py` described above, is what makes
the file executable and self-extracting.

# Deploying an artifact

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
