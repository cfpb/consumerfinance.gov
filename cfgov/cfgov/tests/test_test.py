from __future__ import print_function

import six
import sys
from six import StringIO
from unittest import TestCase, TestSuite, defaultTestLoader

from cfgov.test import StdoutCapturingTestRunner, redirect_stdout


if six.PY2:
    class TestRedirectStdout(TestCase):

        def test_redirect_to_string_io(self):
            stdout = sys.stdout
            unstdout = StringIO()
            with redirect_stdout(unstdout):
                self.assertIs(sys.stdout, unstdout)
                print('Hello, world!', file=sys.stdout)

            self.assertIs(sys.stdout, stdout)
            test_str = unstdout.getvalue().strip()
            self.assertEqual(test_str, 'Hello, world!')

        def test_raises_exception(self):
            unstdout = StringIO()
            with self.assertRaises(ValueError):
                with redirect_stdout(unstdout):
                    raise ValueError('Test exception handling')


class TestStdoutCapturingTestRunner(TestCase):

    def test_with_stdout(self):
        class LoudTestCase(TestCase):
            def test(self):
                print('True is true, who knew!')
                self.assertTrue(True)

        loud_suite = TestSuite(
            tests=defaultTestLoader.loadTestsFromTestCase(LoudTestCase)
        )

        with self.assertRaises(AssertionError):
            StdoutCapturingTestRunner(verbosity=0).run_suite(
                loud_suite,
                stream=StringIO()
            )

    def test_with_no_stdout(self):
        class QuietTestCase(TestCase):
            def test(self):
                self.assertTrue(True)

        quiet_suite = TestSuite(
            tests=defaultTestLoader.loadTestsFromTestCase(QuietTestCase)
        )

        # Supress test case output while this runs so we don't get weird
        # test-case-in-our-test-case messaging
        result = StdoutCapturingTestRunner().run_suite(
            quiet_suite,
            stream=StringIO()
        )

        # No errors should be raised and the suite should have passed
        self.assertEqual(result.errors, [])
        self.assertEqual(result.failures, [])
