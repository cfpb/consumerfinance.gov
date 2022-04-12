import os
import shutil
import tempfile
from unittest import TestCase, mock

from deployable_zipfile.extract import (
    extract_zipfile,
    locate_virtualenv_site_packages,
)


class TestLocateVirtualenvSitePackages(TestCase):
    @mock.patch("subprocess.check_output", return_value=b"somewhere\n")
    def test_calls_python_to_print_path(self, check_output):
        python_executable = "/path/to/python"

        # This should return the stripped result of the Python call.
        self.assertEqual(
            locate_virtualenv_site_packages(python_executable), "somewhere"
        )

        # This should have called Python to print the last element in the path.
        check_output.assert_called_once_with(
            [python_executable, "-c", "import sys; print(sys.path[-1])"]
        )


class TestExtractZipFile(TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tempdir)

    @mock.patch("subprocess.check_call")
    def test_extract_zipfile(self, check_call):
        test_data = os.path.join(os.path.dirname(__file__), "data")
        test_zip = os.path.join(test_data, "test.zip")

        extract_location = os.path.join(self.tempdir, "extracted")

        # Since we're not really creating a virtual environment, we mock the
        # location of site-packages so we can confirm the files that should
        # be copied there.
        site_packages = os.path.join(extract_location, "site-packages")
        os.makedirs(site_packages)

        with mock.patch(
            "deployable_zipfile.extract.locate_virtualenv_site_packages",
            return_value=site_packages,
        ):
            extract_zipfile(test_zip, extract_location)

        # Verify that all files are extracted properly, that the appropriate
        # files are copied to site-packages, and that all unnecessary files are
        # cleaned up from the extract location.
        self.assertCountEqual(
            [
                os.path.join(root, name)
                for root, __, files in os.walk(extract_location)
                for name in files
            ],
            [
                os.path.join(extract_location, f)
                for f in [
                    "deployable_zip/foo.txt",
                    "deployable_zip/subdir/bar.txt",
                    "site-packages/deployable_zip.pth",
                    "site-packages/loadenv.pth",
                    "site-packages/loadenv.py",
                ]
            ],
        )
