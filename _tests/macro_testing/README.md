# Jinja2 Macro Unit Tests

This is a collection of unit tests for this repository's Jinja2 macros
and the utilities to run them. 

## Running the Tests

To ensure that the Python dependencies for the test runner are installed
you'll want to run:

```shell
$ pip install -r requirements.txt
```

This should probably be done from within the Python virtualenv being
used for cfgov-refresh.

Once the requirements are installed, the tests can be run with 
`runner.py`:

```shell
$ python runner.py
```

This will run tests defined in JSON files in the [`tests`](tests) 
subdirectory.

## Writing Unit Tests for Jinja2 Macros

There are two ways that unit tests for Jinja2 macros can be written,
in Python and in a JSON file.

### JSON Test Specifications

To reduce the amount of boilerplate Python that needs to be written for
macro unit tests, unit tests can be writen in JSON.

For each template file that defines macros, a single JSON should be
created that would look like this:

```json
{
    "file": "macros.html",
    "tests": [
        {
            "macro_name": "my_macro",
            ...
        },
        { ... },
    ]
}
```

**`file`** is the template file. The test environment uses the same
mechanism that Sheer uses to lookup template files, so the same file
specification that's used within templates that use the macros.

**`tests`** is a list of individual test case specifications. These
corrospond to a single macro.

The specification for a test case for an individual macro looks like
this:

```json
{
    "macro_name": "<a macro>",
    "arguments": [ ... ],
    "keyword_arguments": { ... },
    "filters": {
        "<filter name>": "<mock value>",
        "<filter name>": ["<first call mock value>",
                            "<second call mock value>", ...]
    },
    "context_functions": {
        "<function name>": "<mock value>",
        "<function name>": ["<first call mock value>",
                            "<second call mock value>", ...]
    },
    "assertions": [
        {
            "selector": "<css selector>",
            "index": <1>,
            "assertion": "<equal>",
            "value": "<string contained>"
        }
    ]
}
```

**`macro_name`** is simply the name of the macro within the file in which it
is defined.

**`arguments`** is a list of arguments to pass to the macro in the order
they are given. This is optional.

**`keyword_arguments`** is an object containing key/value arguments to pass
to the macro if it requires keyword arguments. This is optional.

**`filters`** is an object that is used to mock Jinja2 filters. It contains
the name of the filter to be mocked and the value that should be
returned when that filter is used. The value can also be a list, in
which case the order of the list will corropsond to the order in which
the filter is called, i.e. if you want the filter to return `1` the
first time it is called, but `2` the second time, the value would be
`[1, 2]`. This is optional.

*Note:* Here are some Sheer filters you may want to consider mocking:

- `selected_filters_for_field`
- `is_filter_selected`

**`context_functions`** is an object that is used to mock Jinja2 context
functions. It works the same way that `filters` does above, with the
values either being a return value for all calls or a list of return
values for each call. This is optional.

*Note:* Here are some Sheer context functions you may want to consider
mocking:

- `queries`
- `more_like_this`
- `get_document`

**`assertions`** defines the assertions to make about the result of
rendering the macro. Assertion definitions take a CSS `selector`, an 
`index` in the list of matches for that selector (default is `0`), an 
`assertion` to make an  a `value` for comparison (if necessary for the 
assertion).

The `assertion` can be any of the following:

- `equal`
- `not equal`
- `true`
- `false`
- `exists`
- `in`
- `not in`

Multiple test cases can be defined for the same macro, to test different
behavior with different inputs, filter or context funciton output.

### Python Test Cases

If there is a more complex scenario you would like to test that cannot
be described by the JSON specification format, you can create a test
case in Python. 


These unit tests are all based on Python's 
[`unittest`](https://docs.python.org/2/library/unittest.html) module. 
All of the Macro test cases inherit from the class `MacroTestCase`, 
defined in `macrotest.py`. This class sets up the Jinja2 environment 
for unittesting and provides some convenience methods for mocking 
Jinja2 filters, context functions, and for rendering the macro. 

```python
from macrotest import MacroTestCase

class MyMacrosTestCase(MacroTestCase):

    def test_a_macro(self):
        mock_filter(...)
        mock_context_function(...)
        result = self.render_macro('mymacros.html', 'amacro')
        assert 'something' in result.select('.css-selector')
````

