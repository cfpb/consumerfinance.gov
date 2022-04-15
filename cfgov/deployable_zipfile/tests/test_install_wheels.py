import os
import shutil
import tempfile
from unittest import TestCase, mock

from deployable_zipfile.install_wheels import install_wheels


class TestSetup(TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tempdir)

    @mock.patch("subprocess.check_call")
    def test_something(self, check_call):
        wheel_directory = os.path.join(
            os.path.dirname(__file__), "data", "wheels"
        )

        install_wheels(wheel_directory)

        # We expect that only compatible wheels will be installed.

        expected_wheels = ["baz-1.0-py3-none-any.whl"]

        expected_wheels.append("foo-1.0-py2.py3-none-any.whl")

        # We expect that subprocess.check_call() is called once and passed a
        # list of arguments, the first of which is the path to Python.
        self.assertEqual(check_call.call_count, 1)
        _, args, __ = check_call.mock_calls[0]
        self.assertEqual(len(args), 1)

        self.assertEqual(
            args[0][1:],
            ["-m", "pip", "install", "--no-deps"]
            + [os.path.join(wheel_directory, f) for f in expected_wheels],
        )
