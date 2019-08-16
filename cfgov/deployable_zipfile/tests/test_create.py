import os
import shutil
import sys
import tempfile
from unittest import TestCase
from zipfile import ZipFile

import mock
from scripts.create_deployable_zip import create_zipfile, save_wheels


class TestSaveWheels(TestCase):
    @mock.patch('subprocess.check_call')
    def test_save_wheels_calls_pip_wheel(self, check_call):
        save_wheels(
            '/destination/path',
            'django',
            'wagtail',
            '-rrequirements.txt'
        )

        check_call.assert_called_once_with([
            sys.executable,
            '-m',
            'pip',
            'wheel',
            '--wheel-dir=/destination/path',
            'django',
            'wagtail',
            '-rrequirements.txt',
        ])

    @mock.patch('subprocess.check_call', side_effect=RuntimeError)
    def test_save_wheels_re_raises_pip_wheel_exception(self, check_call):
        with self.assertRaises(RuntimeError):
            save_wheels('/destination/path')


class TestCreateDeployableZip(TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()

        test_data = os.path.join(os.path.dirname(__file__), 'data')

        self.zip_source = os.path.join(test_data, 'deployable_zip')
        self.requirements_file = os.path.join(test_data, 'requirements.txt')

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    @mock.patch('scripts.create_deployable_zip.save_wheels')
    def test_create_zipfile(self, save_wheels):
        zipfile_basename = os.path.join(self.tempdir, 'archive')

        zipfile_filename = create_zipfile(
            self.zip_source,
            self.requirements_file,
            zipfile_basename
        )

        # save_wheels should be called twice; once for the bootstrap wheels
        # (virtualenv, pip, setuptools) and once for the requirements file.
        self.assertEqual(save_wheels.call_count, 2)

        self.assertEqual(zipfile_filename, '%s.zip' % zipfile_basename)

        archive = ZipFile(zipfile_filename)
        self.assertEqual(sorted(archive.namelist()), [
            'deployable_zip/',
            'deployable_zip/foo.txt',
            'deployable_zip/subdir/',
            'deployable_zip/subdir/bar.txt',
        ])
