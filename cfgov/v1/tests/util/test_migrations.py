from django.test import TestCase

from v1.util.migrations import (
    MoveContactPhoneFaxToPhonesOperation,
    RegexAlterBlockValueOperation,
)


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


class MoveContactPhoneFaxToPhonesOperationTestCase(TestCase):
    def setUp(self):
        self.operation = MoveContactPhoneFaxToPhonesOperation()

    def test_fax_true_is_applied_to_every_number(self):
        value = {
            "fax": True,
            "phones": [
                {"type": "item", "value": {"number": "1"}, "id": "a"},
                {"type": "item", "value": {"number": "2"}, "id": "b"},
            ],
        }
        self.assertEqual(
            self.operation.apply(value),
            {
                "phones": [
                    {
                        "type": "item",
                        "value": {"number": "1", "is_fax": True},
                        "id": "a",
                    },
                    {
                        "type": "item",
                        "value": {"number": "2", "is_fax": True},
                        "id": "b",
                    },
                ]
            },
        )

    def test_fax_false_or_missing_is_applied_to_every_number(self):
        for value in (
            {"fax": False, "phones": [{"type": "item", "value": {}}]},
            {"phones": [{"type": "item", "value": {}}]},
        ):
            with self.subTest(value=value):
                self.assertEqual(
                    self.operation.apply(value),
                    {"phones": [{"type": "item", "value": {"is_fax": False}}]},
                )

    def test_legacy_list_items_without_wrapper(self):
        self.assertEqual(
            self.operation.apply({"fax": True, "phones": [{"number": "1"}]}),
            {"phones": [{"number": "1", "is_fax": True}]},
        )

    def test_no_phones(self):
        self.assertEqual(self.operation.apply({"fax": True}), {})
