# -*- coding: utf-8 -*-

import os, os.path
import sys
import unittest

from macrotest import JSONSpecMacroTestCaseFactory


def JSONTestCaseLoader(tests_path, recursive=False):
    """
    Load JSON specifications for Jinja2 macro test cases from the given
    path and returns the resulting test classes.

    This function will create a MacroTestCase subclass (using
    JSONSpecMacrosTestCaseFactory) for each JSON file in the given path.

    If `recursive` is True, it will also look in subdirectories. This is
    not yet supported.
    """

    json_files = [f for f in os.listdir(tests_path) if f.endswith('.json')]
    for json_file in json_files:
        # Create a camelcased name for the test. This is a minor thing, but I
        # think it's nice.
        name, extension = os.path.splitext(json_file)
        class_name = ''.join(x for x in name.title() if x not in ' _-') + 'TestCase'

        # Get the full path to the file and create a test class
        json_file_path = os.path.join(tests_path, json_file)
        test_class = JSONSpecMacroTestCaseFactory(class_name, json_file_path)

        # Add the test class to globals() so that unittest.main() picks it up
        globals()[class_name] = test_class


if __name__ == '__main__':
    JSONTestCaseLoader('./tests/')
    unittest.main()


