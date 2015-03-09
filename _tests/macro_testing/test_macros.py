#!/usr/bin/env python

import unittest
import os.path
from macropolo import MacroTestCase, JSONTestCaseLoader
from macropolo.environments import SheerEnvironment

class CFGovTestCase(SheerEnvironment, MacroTestCase):
    """
    A MacroTestCase subclass for cfgov-refresh.
    """

    def search_root(self):
        """
        Return the root of the search path for templates.
        """
        # Get the cfgov-refresh root dir, ../../../
        # PLEASE NOTE: This presumes that the file containing the test always
        # lives three levels above the cfgov-refresh root.
        root_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ),
                                                os.pardir, os.pardir))
        return root_dir


    def search_exceptions(self):
        """
        Return a list of a subdirectory names that should not be searched
        for templates.
        """
        return ['_defaults', '_lib', '_queries', '_settings', '_tests']


# Create CFGovTestCase subclasses for all JSON tests.
tests_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'tests'))
JSONTestCaseLoader(tests_path, CFGovTestCase, globals())


# Run the tests if we're executed
if __name__ == '__main__':
    unittest.main()


