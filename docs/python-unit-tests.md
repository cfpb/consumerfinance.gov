# Backend testing

## Writing tests

We have multiple resources for writing new unit tests for Django, Wagtial, and Python code:

- [CFPB Django and Wagtail unit testing documentation](https://github.com/cfpb/development/blob/master/guides/unittesting-django-wagtail.md)
- [The Django testing documentation](https://docs.djangoproject.com/en/1.11/topics/testing/overview/)
- [The Wagtail testing documentation](http://docs.wagtail.io/en/v1.13.4/advanced_topics/testing.html)
- [Real Python's "Testing in Django"](https://realpython.com/testing-in-django-part-1-best-practices-and-examples/)

## Running tests

To run the the full suite of Python tests using Tox, 
make sure you are in the cfgov-refresh root and then run:

```sh
tox
```

This will run linting tests and unit tests with migrations in Python. 
This is the same as running:

```sh
tox -e lint -e unittest-py36-dj111-wag113-slow
```

By default this uses a local SQLite database for tests. To override this, you
can set the `TEST_DATABASE_URL` environment variable to a database connection
string as supported by [dj-database-url](https://github.com/kennethreitz/dj-database-url).

If you haven't changed any Python dependencies and you don't need to test 
all migrations, you can run a much faster Python code test using:

```sh
# Python
tox -e unittest-py36-dj111-wag113-fast
```

If you would like to run only a specific test, or the tests for a specific app, 
you can provide a dotted path to the test as the final argument to any of the above calls to `tox`:

```sh
tox -e unittest-py36-dj111-wag113-fast regulations3k.tests.test_regdown
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
TEST_RUNNER=cfgov.test.StdoutCapturingTestRunner tox -e fast
```

This test runner is enabled when tests are run automatically on [Travis CI](https://travis-ci.org/),
but is not used by default when running tests locally.


## GovDelivery

If you write Python code that interacts with the GovDelivery subscription API, you can use the functionality provided in `core.govdelivery.MockGovDelivery` as a mock interface to avoid the use of `patch` in unit tests.

This object behaves similarly to the real `govdelivery.api.GovDelivery` class in that it handles all requests and returns a valid (200) `requests.Response` instance.

Conveniently for unit testing, all calls are stored in a class-level list that can be retrieved at `MockGovDelivery.calls`. This allows for testing of code that interacts with GovDelivery by checking the contents of this list to ensure that the right methods were called.

This pattern is modeled after Django's [`django.core.mail.outbox`](https://docs.djangoproject.com/en/2.0/topics/testing/tools/#email-services) which provides similar functionality for testing sending of emails.

The related classes `ExceptionMockGovDelivery` and `ServerErrorMockGovDelivery` can similarly be used in unit tests to test for cases where a call to the GovDelivery API raises an exception and returns an HTTP status code of 500, respectively.
