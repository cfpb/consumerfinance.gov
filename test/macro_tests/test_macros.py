#!/usr/bin/env python

import unittest
import sys
import os, os.path

from unipath import Path

from macropolo import MacroTestCase, JSONTestCaseLoader
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cfgov.settings.test')

import django
from django.conf import settings
from django.utils.module_loading import import_string

sys.path.append(Path(__file__).ancestor(3).child('cfgov'))
django.setup()

from macropolo.environments import Jinja2Environment

class CFGovMacroTestEnvironment(Jinja2Environment):
    def setup_environment(self):
        super(CFGovMacroTestEnvironment, self).setup_environment()
        backend_config = settings.TEMPLATES[1].copy()
        backend_cls_name = backend_config.pop('BACKEND')
        backend_cls = import_string(backend_cls_name)
        backend = backend_cls(backend_config)
        env = backend.env
        self.filters = env.filters


class CFGovTestCase(CFGovMacroTestEnvironment, MacroTestCase):
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

        templates = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            os.pardir,
            'cfgov/jinja2/v1'))

        return templates


    def search_exceptions(self):
        """
        Return a list of subdirectory names that should not be searched
        for templates.
        """
        templates = 'cfgov/jinja2/v1'
        return [
            templates + '/_defaults',
            templates + '/_lib',
            templates + '/_queries',
            templates + '/_settings',
            'test',
            'config'
        ]


# Create CFGovTestCase subclasses for all JSON tests.
tests_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'tests'))
JSONTestCaseLoader(tests_path, CFGovTestCase, globals())


# Run the tests if we're executed
if __name__ == '__main__':
    unittest.main()
