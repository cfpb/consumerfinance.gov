This repository includes code for generating a self-zip archive
of the code and all of it's Python dependencies. We use these
archives to deploy the site to a Linux server.

# What's an artifact?

It's a zip file, that is executable and includes a Python "shebang" line. Here's a
(very abbreviated) peek into what's *in* the zip file:

```
__main__.py
cfgov.pth
loadenv.py
setup.py
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

The `__main__.py` file contains [the code that runs when the zipfile is invoked
as a python module](https://github.com/cfpb/cfgov-refresh/blob/master/cfgov/deployable_zipfile/extract.py)

The `wheels/` directory contains all of our python dependencies, while
`bootstrap_wheels` contains modules needed at deployment time, to install
everything.

`loadenv.py` and `loadenv-init.pth` are used to load environment variables from
a `environment.json` file, deployed seperately. An environment.json file l

# Generating a deployment artifact

Running the script at `./docker/deployable-zipfile/build.sh` will start a CentOS 6
container, generate the artifact, and save it to `./cfgov_current_build.zip`.

# Deploying an artifact

We currently use Ansible to prepare servers to run an artifact, and to do the actual deployment.
If we ignore some specifics and quirks of our environment, the basic steps look something like this:

- copy the artifact to the system
- execute the artifact, with the -d (destination) argument, `./artifact.zip -d destination-dir`. This
will unpack the files, create a new virtualenv, install all of the wheels in `wheels/` into that
virtualenv. **Important Note:** This should be done with the same python interpreter that will run the
application. For example, on our servers this means using [`scl enable`](https://linux.die.net/man/1/scl)
to specify a particular Python version from 
[Software Collections](https://www.softwarecollections.org/en/scls/?search=python).
- put an 'environment.json' file in place, in your destination-dir
- run django utilities like 'collectstatic' and 'migrate'
- update a symlink to point to the latest release
- restart your WSGI server.
