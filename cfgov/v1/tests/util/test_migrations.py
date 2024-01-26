from django.test import TestCase

from v1.util.migrations import RegexAlterBlockValueOperation


class RegexAlterBlockValueOperationTestCase(TestCase):
    def setUp(self):
        pattern = r"foo"
        replacement = r"bar"
        self.operation = RegexAlterBlockValueOperation(
            pattern=pattern,
            replacement=replacement,
        )

    def test_regex_alter_value(self):
        self.assertEqual(
            self.operation.apply("Some text with foo in it"),
            "Some text with bar in it",
        )

    def test_regex_does_not_alter_value(self):
        self.assertEqual(
            self.operation.apply("Some text without any"),
            "Some text without any",
        )

    def test_regex_alter_multiple_values(self):
        self.assertEqual(
            self.operation.apply("Some text-foo with multiple foos in it"),
            "Some text-bar with multiple bars in it",
        )
