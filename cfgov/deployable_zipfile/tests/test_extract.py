import os
import shutil
import six
import sys
import tempfile
from unittest import TestCase

import mock
from deployable_zipfile.extract import extract_zipfile


class TestExtractZipFile(TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    @mock.patch('subprocess.check_call')
    def test_extract_zipfile(self, check_call):
        test_data = os.path.join(os.path.dirname(__file__), 'data')
        test_zip = os.path.join(test_data, 'deployable_with_wheels.zip')

        extract_location = os.path.join(self.tempdir, 'extracted')
        extract_zipfile(test_zip, extract_location)

        # Verify that all files are extracted properly.
        six.assertCountEqual(
            self,
            [
                os.path.join(root, name)
                for root, __, files in os.walk(extract_location)
                for name in files
            ],
            [
                os.path.join(extract_location, f) for f in [
                    'deployable_zip/foo.txt',
                    'deployable_zip/subdir/bar.txt',
                    'wheels/test-0.0.1-py2.py3-none-any.whl',
                ]
            ]
        )

        # Verify that the virtual environment was created and that the setup
        # script was called appropriately.
        check_call.assert_has_calls([
            # First call should create the virtual environment.
            mock.call([
                sys.executable,
                '-m',
                'virtualenv',
                '--never-download',
                '--no-wheel',
                '--extra-search-dir=%s' % os.path.join(
                    extract_location,
                    'bootstrap_wheels'
                ),
                os.path.join(extract_location, 'venv'),
            ]),

            # Second call should invoke the setup script using the Python
            # binary in the virtual environment.
            mock.call([
                os.path.join(extract_location, 'venv', 'bin', 'python'),
                os.path.join(extract_location, 'install_wheels.py'),
            ])
        ])
