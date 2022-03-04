# Python testing

## Writing tests

We have multiple resources for writing new unit tests for Django, Wagtail, and Python code:

- [CFPB Django and Wagtail unit testing documentation](https://github.com/cfpb/development/blob/main/guides/unittesting-django-wagtail.md)
- [The Django testing documentation](https://docs.djangoproject.com/en/1.11/topics/testing/overview/)
- [The Wagtail testing documentation](http://docs.wagtail.io/en/stable/advanced_topics/testing.html)
- [Real Python's "Testing in Django"](https://realpython.com/testing-in-django-part-1-best-practices-and-examples/)

### Testing Elasticsearch

When writing tests that rely on a running Elasticsearch service, consider using the
[`search.elasticsearch_helpers.ElasticsearchTestsMixin`](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/search/elasticsearch_helpers.py)
mixin:

```py
from django.test import TestCase

from search.elasticsearch_helpers import ElasticsearchTestsMixin


class MyTests(ElasticsearchTestsMixin, TestCase):
    def test_something(self):
        self.rebuild_elasticsearch_index()

        # test something that relies on the Elasticsearch index
```

Refer to the mixin's
[source code](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/search/elasticsearch_helpers.py)
for additional details on its functionality.

## Prerequisites

If you have set up
[a standalone installation of consumerfinance.gov](/installation/#install-system-level-requirements),
you'll need to
[activate your virtual environment](/running-virtualenv/#3-launch-site)
before running the tests:

```sh
workon consumerfinance.gov
```

If you have not set up the standalone installation of consumerfinance.gov,
you can still run the tests if you install Tox in your
[local installation of Python](https://github.com/cfpb/development/blob/main/guides/installing-python.md):

```
pip install tox
```

If you have set up
[a Docker-based installation of consumerfinance.gov](/installation/#docker-based-installation),
you can run the tests there by
[accessing the Python container's shell](http://localhost:8888/running-docker/#access-a-containers-shell):

```sh
docker-compose exec python bash
```

## Running tests

Our test suite can either be run in a local virtualenv or in Docker.
Please note, the tests run quite slow in Docker.

To run the the full suite of Python tests using Tox,
make sure you are in the consumerfinance.gov root and then run:

```sh
tox
```

Tox runs different isolated Python environments with different versions of dependencies.
We use it to format and lint our Python files, check out import sorting, and run unit tests
in Python 3.8.
You can select specific environments using `-e`.

Running `tox` by itself is the same as running:

```sh
tox -e lint -e unittest
```

These default environments are:

- `lint`, which runs our [linters](#linting). We require this
  environment to pass in CI.
- `validate-migrations`, which checks for any missing Django migrations.
  We require this environment to pass in CI.
- `unittest`, which runs unit tests against the current production
  versions of Python, Django, and Wagtail. We require this environment to
  pass in CI.

Tests will run against the default Django database.

If you would like to run only a specific test, or the tests for a specific app,
you can provide a dotted path to the test as the final argument to any of the above calls to `tox`:

```sh
tox -e unittest regulations3k.tests.test_regdown
```

If you would like to skip running Django migrations when testing, set the
`SKIP_DJANGO_MIGRATIONS` environment variable to any value before running `tox`.


### Formatting
We use `black` to autoformat our Python code. `black` is invoked by Tox using 
the `lint` environment (this will also run `flake8` and `isort`):

```sh
tox -e lint
```

**It is highly recommended to only invoke black via tox**


### Linting

We use the `flake8` and `isort` tools to ensure compliance with
[PEP8 style guide](https://www.python.org/dev/peps/pep-0008/),
[Django coding style guidelines](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/),
and the
[CFPB Python style guide](https://github.com/cfpb/development/blob/main/standards/python.md#linting).

Both `flake8` and `isort` can be run using the Tox `lint` environment (this 
will also run `black`):

```sh
tox -e lint
```

This will run `isort` in check-only mode and it will print diffs for imports
that need to be fixed. To automatically fix import sort issues, run:

```sh
isort --recursive cfgov/
```

From the root of `consumerfinance.gov`.

### Coverage

To see Python code coverage information immediately following a test run, 
you can add the `coverage` env to the list of envs for tox to run:

```sh
tox -e lint -e unittest -e coverage
```

You can also run coverage directly to see coverage information from a previous test run:

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
TEST_RUNNER=core.testutils.runners.StdoutCapturingTestRunner tox -e unittest
```

This test runner is enabled when tests are run automatically on
[GitHub Actions](../github-actions/),
but is not used by default when running tests locally.


## GovDelivery

If you write Python code that interacts with the GovDelivery subscription API, you can use the functionality provided in `core.govdelivery.MockGovDelivery` as a mock interface to avoid the use of `patch` in unit tests.

This object behaves similarly to the real `govdelivery.api.GovDelivery` class in that it handles all requests and returns a valid (200) `requests.Response` instance.

Conveniently for unit testing, all calls are stored in a class-level list that can be retrieved at `MockGovDelivery.calls`. This allows for testing of code that interacts with GovDelivery by checking the contents of this list to ensure that the right methods were called.

This pattern is modeled after Django's [`django.core.mail.outbox`](https://docs.djangoproject.com/en/2.0/topics/testing/tools/#email-services) which provides similar functionality for testing sending of emails.

The related classes `ExceptionMockGovDelivery` and `ServerErrorMockGovDelivery` can similarly be used in unit tests to test for cases where a call to the GovDelivery API raises an exception and returns an HTTP status code of 500, respectively.
