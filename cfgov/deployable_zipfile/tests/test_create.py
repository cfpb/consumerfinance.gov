import os
import shutil
import sys
import tempfile
from unittest import TestCase, mock
from zipfile import ZipFile

from deployable_zipfile.create import create_zipfile, save_wheels


class TestSaveWheels(TestCase):
    @mock.patch("subprocess.check_call")
    def test_save_wheels_calls_pip_wheel(self, check_call):
        save_wheels(
            sys.executable,
            "/destination/path",
            "django",
            "wagtail",
            "-rrequirements.txt",
        )

        check_call.assert_called_once_with(
            [
                sys.executable,
                "-m",
                "pip",
                "wheel",
                "--wheel-dir=/destination/path",
                "--find-links=/destination/path",
                "django",
                "wagtail",
                "-rrequirements.txt",
            ]
        )

    @mock.patch("subprocess.check_call", side_effect=RuntimeError)
    def test_save_wheels_re_raises_pip_wheel_exception(self, check_call):
        with self.assertRaises(RuntimeError):
            save_wheels(sys.executable, "/destination/path")


class TestCreateDeployableZip(TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()

        test_data = os.path.join(os.path.dirname(__file__), "data")

        self.zip_source = os.path.join(test_data, "deployable_zip")
        self.requirements_file = os.path.join(test_data, "requirements.txt")
        self.extra_static = os.path.join(test_data, "extra_static")

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    @mock.patch("deployable_zipfile.create.save_wheels")
    def test_create_zipfile(self, save_wheels):
        zipfile_basename = os.path.join(self.tempdir, "archive")

        zipfile_filename = create_zipfile(
            self.zip_source,
            self.requirements_file,
            zipfile_basename,
            extra_static=[self.extra_static],
            extra_python="python4",
        )

        # save_wheels should be called three times; once for the bootstrap
        # wheels (pip, setuptools), and once per Python version for the
        # requirements file.
        self.assertEqual(save_wheels.call_count, 3)

        self.assertEqual(zipfile_filename, "%s.zip" % zipfile_basename)

        archive = ZipFile(zipfile_filename)
        self.assertCountEqual(
            archive.namelist(),
            [
                "__main__.py",
                "deployable_zip.pth",
                "deployable_zip/",
                "deployable_zip/foo.txt",
                "deployable_zip/subdir/",
                "deployable_zip/subdir/bar.txt",
                "install_wheels.py",
                "loadenv-init.pth",
                "loadenv.py",
                "static.in/",
                "static.in/0/",
                "static.in/0/extra.css",
            ],
        )
