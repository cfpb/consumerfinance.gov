# -*- coding: utf-8 -*-
"""
This is the base of our macro unittesting suite. It contains helpers
that should make unittesting Jinja2 macros a little easier.
"""

import os.path
import unittest

from jinja2 import Environment, FileSystemLoader
from jinja2 import Template

# We'll use the same code Sheer uses to build the filesystem template search
# path.
from sheer.utility import build_search_path
from sheer.templates import date_formatter
import markdown

def code_capture():
    env = Environment(loader=PackageLoader('yourapplication', 'templates'))
    template = env.get_template('mytemplate.html')
    template.render(the='variables', go='here')

    template = Template('Hello {{ name }}!')
    template.render(name='John Doe')



class MacroTestCase(unittest.TestCase):
    """
    The `MacroTestCase` class is intended to capture test cases for
    macros on a modular basis, i.e. you would create one subclass of
    `MacroTestCase` for each Jinja2 template file containing macros. That
    That subclass can then include `test_[macro_name]()` methods that
    test each individual macro.

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
                                                os.pardir, os.pardir, os.pardir))
        search_path = build_search_path(root_dir,
                                        search_path,
                                        append=['_layouts', '_includes'],
                                        include_start_directory=True)
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
        arguments.

        Internally method will construct a simple string template that
        calls the macro and renders that template and returns the
        result.
        """
        # We need to format args and kwargs as string arguments for the macro.
        # After that we combine them. filter() is used in case one or the other
        # strings is empty, ''.
        str_args = ', '.join(str(a) for a in args)
        str_kwargs = ', '.join('%s=%r' % x for x in kwargs.iteritems())
        str_combined = ', '.join(filter(None, [str_args, str_kwargs]))

        # Here is our test template that uses the macro.
        test_template_str = '''{%% import "%s" as macro_file %%}
{{ macro_file.%s(%s) }}''' % (macro_file, macro, str_combined)
        test_template = self.env.from_string(test_template_str)

        result = test_template.render(self.context)
        return result


class PostMacrosTestCase(MacroTestCase):

    def setUp(self):
        self.setup_environment()

    def test_posts_summary(self):
        result = self.render_macro('post-macros.html', 'post_summary',
                                   {'title': 'Test Post',
                                    'dek': 'A dek',
                                    'excerpt': 'An excerpt',
                                    'author': ['Me',]})
        assert 'Test Post' in result



if __name__ == '__main__':
    unittest.main()

