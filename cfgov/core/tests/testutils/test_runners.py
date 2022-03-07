from io import StringIO
from unittest import TestCase, TestSuite, defaultTestLoader

from core.testutils.runners import StdoutCapturingTestRunner


class StderrSuppressingStdoutCapturingTestRunner(StdoutCapturingTestRunner):
    """Modified StdoutCapturingTestRunner for use in testing.

    Normally when tests are run, they write output to stderr indicating
    how many tests are run, and whether they succeed, like this:

    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.000s

    OK

    For the purposes of testing our test runner, we want to suppress
    this output, so that we don't get test case output within our test
    case output.

    We do this by capturing stderr while the tests are run. Note that this
    is independent of stdout output, which is what we are actually testing.
    """

    def get_test_runner_kwargs(self):
        kwargs = super().get_test_runner_kwargs()
        kwargs["stream"] = StringIO()
        return kwargs


class TestStdoutCapturingTestRunner(TestCase):
    def _run_suite(self, suite):
        runner = StderrSuppressingStdoutCapturingTestRunner()
        return runner.run_suite(suite)

    def test_with_stdout(self):
        class LoudTestCase(TestCase):
            def test(self):
                print("True is true, who knew!")
                self.assertTrue(True)

        loud_suite = TestSuite(
            tests=defaultTestLoader.loadTestsFromTestCase(LoudTestCase)
        )

        with self.assertRaises(RuntimeError):
            self._run_suite(loud_suite)

    def test_with_no_stdout(self):
        class QuietTestCase(TestCase):
            def test(self):
                self.assertTrue(True)

        quiet_suite = TestSuite(
            tests=defaultTestLoader.loadTestsFromTestCase(QuietTestCase)
        )
        result = self._run_suite(quiet_suite)

        # No errors should be raised and the suite should have passed
        self.assertEqual(result.errors, [])
        self.assertEqual(result.failures, [])
