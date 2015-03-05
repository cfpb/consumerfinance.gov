# -*- coding: utf-8 -*-
"""
This is the base of our macro unittesting suite. It contains helpers
that should make unittesting Jinja2 macros a little easier.
"""

# from __future__ import unicode_literals

import os, os.path
import unittest

from jinja2 import Environment, FileSystemLoader

# We'll use BeautifulSoup to make assertions about the HTML resulting from
# macros
from bs4 import BeautifulSoup

import json

# We'll use the same code Sheer uses to build the filesystem template search
# path.
from sheer.utility import build_search_path
from sheer.templates import date_formatter
import markdown

class MacroTestCase(unittest.TestCase):
    """
    The `MacroTestCase` class is intended to capture test cases for
    macros on a modular basis, i.e. you would create one subclass of
    `MacroTestCase` for each Jinja2 template file containing macros. That
    That subclass can then include `test_[macro_name]()` methods that
    test each individual macro.

    render_macro() returns a BeautifulSoup object that you can then use
    CSS selectors on to make assertions. See
    http://www.crummy.com/software/BeautifulSoup/bs4/doc/#css-selectors

        ```
        class MyMacrosTestCase(MacroTestCase):
            def test_amacro(self):
                mock_filter(...)
                mock_context_function(...)
                result = self.render_macro('mymacros.html', 'amacro')
                assert 'something' in result
        ````

    """

    def setup_environment(self, search_path='/'):
        """
        Set up a Jinja2 environment that mocks the one created by Sheer.
        """
        # Get the cfgov-refresh root dir, ../../../
        # PLEASE NOTE: This presumes that the file containing the test always
        # lives three levels above the cfgov-refresh root.
        root_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ),
                                                os.pardir, os.pardir))
        underscore_exceptions = ['_layouts', '_includes']
        search_path = build_search_path(root_dir,
                                        search_path,
                                        append=underscore_exceptions,
                                        include_start_directory=True)

        # BUT this search path isn't complete... because Sheer includes the
        # request directory in the search path. To try to emulate that we'll add
        # all non-ignored subdirectories.
        search_path += [x[0] for x in os.walk(root_dir)
                        if not x[0].startswith('_') or x[0].startswith('.') or
                            x[0] in underscore_exceptions]

        self.env = Environment(loader=FileSystemLoader(search_path))

        # Sheer filters that are added to the default. These are generally
        # filters we don't need to worry about mocking. We'll mock Sheer filters
        # that return data from Elasticsearch with `mock_filter()` on a
        # macro-by-macro basis. Using lambdas here for brevity.
        # XXX: We should change Sheer to make it easier to replicate its
        # environment.
        self.env.filters['date'] = lambda value, format="%Y-%m-%d": date_formatter(value, format)
        self.env.filters['markdown'] = lambda raw_text: markdown.markdown(raw_text)

        # This is our template context. You can use mock_context_function()
        # below to mock context functions, or you can add values to this
        # dictionary directly.
        self.context = {}


    def setUp(self):
        self.setup_environment()


    def mock_filter(self, filter, **values):
        """
        Mock a Jinja2 filter. This will create a mock function for the
        filter that will return either a single value, or will return
        each of the given values in turn if there are more than one.

        Sheer filters you might want to mock:
            selected_filters_for_field
            is_filter_selected

        """
        mock_filter = Mock()

        if len(values) > 1:
            mock_filter.side_effect = values
        elif len(values) == 1:
            mock_filter.return_value = values[0]

        self.env.filters[filter] = mock_filter


    def mock_context_function(self, func, **values):
        """
        Mock a context function. This will create a mock function that
        will return either a single value, or will return each of the
        given values in turn if there are more than one.

        Sheer context functions you might want to mock:
            queries
            more_like_this
            get_document
        """
        mock_func = Mock()

        if len(values) > 1:
            mock_func.side_effect = values
        elif len(values) == 1:
            mock_func.return_value = values[0]

        self.context[func] = mock_func


    def render_macro(self, macro_file, macro, *args, **kwargs):
        """
        Render a given macro with the given arguments and keyword
        arguments. Returns a BeautifulSoup object.

        Internally method will construct a simple string template that
        calls the macro and renders that template and returns the
        result.
        """
        # We need to format args and kwargs as string arguments for the macro.
        # After that we combine them. filter() is used in case one or the other
        # strings is empty, ''.
        str_args = u', '.join('%r'.encode('utf-8') % a for a in args).encode('utf-8')
        str_kwargs = u', '.join('%s=%r' % x for x in kwargs.iteritems())
        str_combined = u', '.join(filter(None, [str_args, str_kwargs]))

        # Here is our test template that uses the macro.
        test_template_str = u'''{%% import "%s" as macro_file %%}{{ macro_file.%s(%s) }}''' % (macro_file, macro, str_combined)
        test_template = self.env.from_string(test_template_str)

        result = test_template.render(self.context)
        return BeautifulSoup(result)


    def make_assertion(self, result, selector, index=0, assertion='exists', value=None):
        """
        Make an assertion based on the BeautifulSoup result object.

        This method will find the given CSS selector, and make the given
        assertion about the selector's match at the given index. If the
        assertion requires a value to compare to, it should be given.
        """
        selection = result.select(selector)

        if assertion == 'equal':
            assert value == selection[index]
        elif assertion == 'not equal':
            assert value != selection[index]
        elif assertion == 'exists':
            assert len(selection) > index
        elif assertion == 'in':
            assert value in selection[index]
        elif assertion == 'not in':
            assert value not in selection[index]


def JSONSpecMacroTestCaseFactory(name, json_file):
    """
    This factory allows the specification of test cases for Jinja2
    macros in JSON files. This should simplify the creation of test
    cases and reduce the amount of boilerplate Python that needs to be
    written for such cases.

    Specification for a test case is:
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
                    "value": "<string contained>",
                "
            ]
        }

    Assertion definitions take a CSS selector, an index in the list of
    matches for that selector (default is 0), the names and mock values
    of any filters or context functions that are used, an assertion,
    and a value for comparison (if necessary for the assertion).

    "arguments", "keyword_arguments", "filters", and
    "context_functions" are optional.

    Assertions can be any of the following:
        * equal
        * not equal
        * true
        * false
        * exists
        * in
        * not in

            *: Not yet supported

    So a JSON file with multiple testcases (should ideall corrospond
    to a ']ngle template file) would look like this:
        {
            "file": "macros.html",
            "tests": [
                {
                    "macro_name": "my_macro",
                    ...

                 },
                 { ... }
            ]
        }
    """
    # This is a function to convert unicode() objects to str() objects that are
    # unicode-encoded. This should above output in our template like "u'foo'"
    # which Jinja2 can't understand.
    def uniconvert(input):
        if isinstance(input, dict):
            return {uniconvert(key): uniconvert(value) for key, value in input.iteritems()}
        elif isinstance(input, list):
            return [uniconvert(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input

    # This function will return a function that can be assigned as a test method
    # for a macro with the given name in the given file with the give test_dict
    # from the JSON spec.
    def create_test_method(macro_file, macro_name, test_dict):
        def test_method(self):
            # Render the macro from the macro file with the given
            # arguments
            args = test_dict.get('arguments', [])
            kwargs = test_dict.get('keyword_arguments', {})

            result = self.render_macro(macro_file, macro_name,
                                    *args, **kwargs)

            # Loop over the assertions given for the test and make them.
            for a in test_dict.get('assertions', []):
                # Selector is required, the others here have defaults.
                selector = a['selector']
                index = a.get('index', 0)
                assertion = a.get('assertion', 'exists')
                value = a.get('value')

                try:
                    self.make_assertion(result, selector, index=index,
                                        assertion=assertion, value=value)
                except AssertionError as e:
                    # Try to provide some more relevent information to the
                    # assertion error, since by default it'll just say the
                    # failure was in make_assertion.
                    assertion_str = ''
                    if value:
                        assertion_str += '"' + value + '" '
                    assertion_str += '"' + assertion + '" "' + \
                        selector + '" selection '

                    e.args += (assertion_str + \
                               'failed in macro ' + macro_name + \
                               ' in ' + macro_file,)
                    raise e

        return test_method

    # Open and read the JSON spec file
    spec = uniconvert(json.loads(open(json_file).read()))

    # This will be our new class's dict containing all its methods, etc
    newclass_dict = {}

    # Go through the json_spec dict and create test methods for each test
    macro_file = spec['file']
    for t in spec['tests']:
        # Create the test method and add it to the class dictionary
        macro_name = t['macro_name']

        method_name = 'test_' + str(spec['tests'].index(t)) + macro_name

        test_method = create_test_method(macro_file, macro_name, t)
        newclass_dict[method_name] = test_method

    # Create and return the new class.
    newclass = type(name, (MacroTestCase,), newclass_dict)
    return newclass



