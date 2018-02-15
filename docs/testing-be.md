# Backend testing

## Django and Python unit tests

To run the the full suite of Python 2.7 unit tests using Tox, cd to the 
project root, make sure the `TOXENV` variable is set in your `.env` file 
and then run:

```
tox
```

If you haven't changed any installed packages and you don't need to test 
all migrations, you can run a much faster Python code test using:
```
tox -e fast
```

To see Python code coverage information, run
```
./show_coverage.sh
```

## Source code linting

We use the `flake8` and `isort` tools to ensure compliance with 
[PEP8 style guide](https://www.python.org/dev/peps/pep-0008/) and the 
[Django coding style guidelines](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/). 
We do make two exceptions to PEP8 that are ignored in our flake8 
configuration:

- `E731`, we allow assignment of lambda expressions
- `W503`, we allow line breaks after binary operators

Both `flake8` and `isort` can be run using the Tox `lint` environment:

```
tox -e lint
```

This will run `isort` in check-only mode and it will print diffs for imports 
that need to be fixed. To automatically fix import sort issues, run:

```
isort --recursive cfgov/
```

From the root of `cfgov-refresh`.

## Python 3 

Both unit tests and linting can be run with Python 3 to aid in our transition. To run with all Django migrations, 

```
tox -e py36
```

or without Django migrations,

```
tox -e fast-py3
```

Existing unit tests that run on code that has not been made compatible with Python 3 may error or fail, but it is possible to run new tests individually with

```
tox -e fast-py3 package.tests.test_my_code
```

To run both `flake8` and `isort` with Python 3, run

```
tox -e lint-py3
```
