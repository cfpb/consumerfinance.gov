import json
import os
import shutil
import tempfile
import unittest
from unittest import mock

from deployable_zipfile.loadenv import loadenv


class TestLoadenv(unittest.TestCase):
    ENVIRONMENT_VARIABLE = '_TEST_LOADENV'

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()

        self.mock_sys_prefix = os.path.join(self.tempdir, 'mock_sys_prefix')
        os.mkdir(self.mock_sys_prefix)
        mock_sys_prefix = mock.patch('sys.prefix', self.mock_sys_prefix)
        mock_sys_prefix.start()
        self.addCleanup(mock_sys_prefix.stop)

        os.environ.pop(self.ENVIRONMENT_VARIABLE, None)

    def tearDown(self):
        shutil.rmtree(self.tempdir)
        os.environ.pop(self.ENVIRONMENT_VARIABLE, None)

    def test_no_file_environment_variable_not_set(self):
        self.assertIsNone(os.environ.get(self.ENVIRONMENT_VARIABLE))
        loadenv()
        self.assertIsNone(os.environ.get(self.ENVIRONMENT_VARIABLE))

    def create_environment_json_file(self, value):
        environment_json_file = os.path.join(self.tempdir, 'environment.json')
        with open(environment_json_file, 'w') as f:
            f.write(json.dumps({self.ENVIRONMENT_VARIABLE: value}))

    def test_file_exists_json_is_loaded(self):
        self.assertIsNone(os.environ.get(self.ENVIRONMENT_VARIABLE))

        self.create_environment_json_file('foo')
        loadenv()

        self.assertEqual(os.environ.get(self.ENVIRONMENT_VARIABLE), 'foo')

    def test_file_overwrites_existing_value(self):
        os.environ[self.ENVIRONMENT_VARIABLE] = 'bar'
        self.assertEqual(os.environ.get(self.ENVIRONMENT_VARIABLE), 'bar')

        self.create_environment_json_file('baz')
        loadenv()

        self.assertEqual(os.environ.get(self.ENVIRONMENT_VARIABLE), 'baz')
