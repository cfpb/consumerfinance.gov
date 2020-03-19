# Python testing

## Writing tests

We have multiple resources for writing new unit tests for Django, Wagtial, and Python code:

- [CFPB Django and Wagtail unit testing documentation](https://github.com/cfpb/development/blob/master/guides/unittesting-django-wagtail.md)
- [The Django testing documentation](https://docs.djangoproject.com/en/1.11/topics/testing/overview/)
- [The Wagtail testing documentation](http://docs.wagtail.io/en/stable/advanced_topics/testing.html)
- [Real Python's "Testing in Django"](https://realpython.com/testing-in-django-part-1-best-practices-and-examples/)

## Prerequisites

If you have set up 
[a standalone installation of cfgov-refresh](/installation/#install-system-level-requirements), 
you'll need to 
[activate your virtual environment](/running-virtualenv/#3-launch-site) 
before running the tests:

```sh
workon cfgov-refresh
```

If have not set up the standalone installation of cfgov-refresh,
it's not necessary to run the tests. 
You can install Tox in your 
[local installation of Python](https://github.com/cfpb/development/blob/master/guides/installing-python.md):

```
pip install tox
```

If you have set up 
[a Docker-based installation of cfgov-refresh](/installation/#docker-based-installation),
you'll need to 
[access the Python container's shell](http://localhost:8888/running-docker/#access-a-containers-shell) 
before running the tests:

```sh
docker-compose exec python3 bash
```

## Running tests

Our test suite can either be run in a local virtualenv or in Docker. 
Please note, the tests run quite slow in Docker.

To run the the full suite of Python tests using Tox, 
make sure you are in the cfgov-refresh root and then run:

```sh
tox
```

Tox runs different isolated Python environments with different versions of dependencies.
We use it to lint our Python files, check out import sorting, and run unit tests
in both Python 3.6 and Python 3.8.
You can select specific environments using `-e`.

Running `tox` by itself is the same as running:

```sh
tox -e lint -e unittest
```

These default environments are:

- `lint`, which runs our [linting](#linting) tools. We require this 
  environment to pass in CI.
- `unittest`, which runs unit tests against the current production 
  versions of Python, Django, and Wagtail. We require this environment to 
  pass in CI.

In addition, we also have this environment:

- `unittest-future`, which runs unit tests against upcoming versions of 
  Python, Django, and Wagtail. We do not require this environment to pass in 
  CI.
 
By default this uses a local SQLite database for tests. To override this, you
can set the `TEST_DATABASE_URL` environment variable to a database connection
string as supported by [dj-database-url](https://github.com/kennethreitz/dj-database-url).

If you would like to run only a specific test, or the tests for a specific app, 
you can provide a dotted path to the test as the final argument to any of the above calls to `tox`:

```sh
tox -e unittest regulations3k.tests.test_regdown
```

### Linting

We use the `flake8` and `isort` tools to ensure compliance with 
[PEP8 style guide](https://www.python.org/dev/peps/pep-0008/),
[Django coding style guidelines](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/),
and the 
[CFPB Python style guide](https://github.com/cfpb/development/blob/master/standards/python.md#linting).

Both `flake8` and `isort` can be run using the Tox `lint` environment:

```sh
tox -e lint
```

This will run `isort` in check-only mode and it will print diffs for imports 
that need to be fixed. To automatically fix import sort issues, run:

```sh
isort --recursive cfgov/
```

From the root of `cfgov-refresh`.

### Coverage

To see Python code coverage information, run

```sh
coverage report -m
```

To see coverage for a limited number of files, 
use the `--include` argument to `coverage` and provide a path to the files you wish to see:

```sh
coverage report -m --include=./cfgov/regulations3k/*
```

## Test output

Python tests should avoid writing to stdout as part of their normal execution.
To enforce this convention, the tests can be run using a custom Django test
runner that fails if anything is written to stdout. This test runner is at
`cfgov.test.StdoutCapturingTestRunner` and can be enabled with the `TEST_RUNNER`
environment variable:

```sh
TEST_RUNNER=cfgov.test.StdoutCapturingTestRunner tox -e unittest
```

This test runner is enabled when tests are run automatically on [Travis CI](https://travis-ci.org/),
but is not used by default when running tests locally.


## GovDelivery

If you write Python code that interacts with the GovDelivery subscription API, you can use the functionality provided in `core.govdelivery.MockGovDelivery` as a mock interface to avoid the use of `patch` in unit tests.

This object behaves similarly to the real `govdelivery.api.GovDelivery` class in that it handles all requests and returns a valid (200) `requests.Response` instance.

Conveniently for unit testing, all calls are stored in a class-level list that can be retrieved at `MockGovDelivery.calls`. This allows for testing of code that interacts with GovDelivery by checking the contents of this list to ensure that the right methods were called.

This pattern is modeled after Django's [`django.core.mail.outbox`](https://docs.djangoproject.com/en/2.0/topics/testing/tools/#email-services) which provides similar functionality for testing sending of emails.

The related classes `ExceptionMockGovDelivery` and `ServerErrorMockGovDelivery` can similarly be used in unit tests to test for cases where a call to the GovDelivery API raises an exception and returns an HTTP status code of 500, respectively.
