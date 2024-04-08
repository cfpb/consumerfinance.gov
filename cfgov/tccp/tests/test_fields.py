from decimal import Decimal

from django.core import serializers
from django.core.exceptions import ValidationError
from django.db import models
from django.test import SimpleTestCase, TestCase
from django.test.utils import isolate_apps

from tccp.fields import CurrencyDecimalField, JSONListField, YesNoBooleanField

from .testapp.models import (
    YEAR_IN_SCHOOL_CHOICES,
    NullableYearsInSchool,
    YearsInSchool,
)


@isolate_apps()
class CurrencyDecimalFieldTests(SimpleTestCase):
    def check_clean(self, value, **kwargs):
        field = CurrencyDecimalField(null=True, blank=True)
        self.assertEqual(
            field.clean(value, None), kwargs.get("expected", value)
        )

    def test_clean_float(self):
        self.check_clean(0.7, expected=Decimal("0.7"))

    def test_clean_float_rounding(self):
        self.check_clean(12.714, expected=Decimal("12.71"))

    def test_clean_float_rounding_up(self):
        self.check_clean(123.715, expected=Decimal("123.72"))

    def test_clean_decimal(self):
        self.check_clean(Decimal("100"))

    def test_clean_decimal_with_decimal_places(self):
        self.check_clean(Decimal("100.00"))

    def test_clean_string(self):
        self.check_clean("100.00", expected=Decimal("100.00"))

    def test_clean_string_with_dollar_sign(self):
        self.check_clean("$100.00", expected=Decimal("100.00"))


@isolate_apps()
class JSONListFieldTests(SimpleTestCase):
    def check_construction(self, **kwargs):
        class TestModel(models.Model):
            field = JSONListField(**kwargs)

        return TestModel().check()

    def test_valid_construction_with_choices(self):
        self.assertFalse(
            self.check_construction(choices=YEAR_IN_SCHOOL_CHOICES)
        )

    def test_invalid_construction_no_choices(self):
        errors = self.check_construction()
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].id, "tccp.E001")

    def check_clean(self, value, **kwargs):
        field = JSONListField(
            choices=YEAR_IN_SCHOOL_CHOICES, null=True, blank=True
        )
        self.assertEqual(
            field.clean(value, None), kwargs.get("expected", value)
        )

    def test_clean_null_valid(self):
        self.check_clean(None, expected=[])

    def test_clean_empty_string_valid(self):
        self.check_clean("", expected=[])

    def test_clean_empty_list_valid(self):
        self.check_clean([])

    def test_clean_list_single_value_valid(self):
        self.check_clean(["FR"])

    def test_clean_list_multiple_values_valid(self):
        self.check_clean(["FR", "SO"])

    def test_clean_single_valid_string_valid(self):
        self.check_clean("FR", expected=["FR"])

    def test_clean_multiple_valid_strings_valid(self):
        self.check_clean("FR; SO", expected=["FR", "SO"])

    def check_clean_fails_validation(self, value):
        with self.assertRaises(ValidationError):
            self.check_clean(value)

    def test_clean_random_string_invalid(self):
        self.check_clean_fails_validation("This is invalid")

    def test_clean_mixed_validity_strings_invalid(self):
        self.check_clean_fails_validation("FR; SO; FOO")

    def test_clean_list_of_invalid_strings_invalid(self):
        self.check_clean_fails_validation(["This", "is", "invalid"])

    def test_clean_list_of_mixed_validity_invalid(self):
        self.check_clean_fails_validation(["FR", "SO", "FOO"])

    def test_clean_list_with_nulls_invalid(self):
        self.check_clean_fails_validation(["FR", "SO", None])

    serialization_test_value = ["FR", "SO"]
    serialization_test_json = (
        '[{"model": "tccp_tests.nullableyearsinschool", "pk": null, '
        '"fields": {"years": ["FR", "SO"]}}]'
    )

    def test_serialization(self):
        instance = NullableYearsInSchool(years=self.serialization_test_value)
        serialized = serializers.serialize("json", [instance])
        self.assertEqual(serialized, self.serialization_test_json)

    def test_deserialization(self):
        instance = list(
            serializers.deserialize("json", self.serialization_test_json)
        )[0].object
        self.assertIsInstance(instance, NullableYearsInSchool)
        self.assertEqual(instance.years, self.serialization_test_value)


class JSONListFieldModelTests(TestCase):
    def check_save_and_refresh(self, value, **kwargs):
        instance = NullableYearsInSchool(years=value)
        instance.save()
        instance.refresh_from_db()
        self.assertEqual(instance.years, kwargs.get("expected", value))

    def test_save_and_refresh_none(self):
        self.check_save_and_refresh(None, expected=[])

    def test_save_and_refresh_none_not_nullable(self):
        instance = YearsInSchool(years=None)
        instance.save()
        instance.refresh_from_db()
        self.assertEqual(instance.years, [])

    def test_save_and_refresh_empty_list(self):
        self.check_save_and_refresh([])

    def test_save_and_refresh_single_value(self):
        self.check_save_and_refresh(["FR"])

    def test_save_and_refresh_multiple_values(self):
        self.check_save_and_refresh(["FR", "SO"])

    def test_save_and_refresh_single_string_value(self):
        self.check_save_and_refresh("FR", expected=["FR"])

    def test_save_and_refresh_multiple_string_values(self):
        self.check_save_and_refresh("FR; SO", expected=["FR", "SO"])

    def test_query_empty_list_valid(self):
        qs = NullableYearsInSchool.objects.filter(years=[])
        self.assertFalse(qs.exists())

        NullableYearsInSchool.objects.create(years=[])
        self.assertTrue(qs.exists())

    def test_query_by_invalid_type(self):
        with self.assertRaises(ValueError):
            YearsInSchool.objects.filter(years=123)

    def test_query_by_equals_string(self):
        YearsInSchool.objects.create(years=["FR"])
        self.assertFalse(YearsInSchool.objects.filter(years="F"))
        self.assertTrue(YearsInSchool.objects.filter(years="FR"))
        self.assertFalse(YearsInSchool.objects.filter(years="FRY"))

    def test_query_by_contains(self):
        YearsInSchool.objects.create(years=["FR"])
        self.assertFalse(YearsInSchool.objects.filter(years__contains="F"))
        self.assertTrue(YearsInSchool.objects.filter(years__contains="FR"))

    def test_query_by_equals_list(self):
        qs = YearsInSchool.objects.filter(years=["FR"])
        self.assertFalse(qs.exists())

        YearsInSchool.objects.create(years=["FR"])
        self.assertTrue(qs.exists())

    def test_values_list(self):
        YearsInSchool.objects.bulk_create(
            [
                YearsInSchool(years=["FR", "SO"]),
                YearsInSchool(years=["JR", "SR"]),
            ]
        )

        self.assertEqual(
            list(YearsInSchool.objects.values_list("years", flat=True)),
            [["FR", "SO"], ["JR", "SR"]],
        )


class YesNoBooleanFieldTests(SimpleTestCase):
    def clean(self, value):
        return YesNoBooleanField().clean(value, None)

    def test_clean_yes(self):
        self.assertTrue(self.clean("Yes"))

    def test_clean_no(self):
        self.assertFalse(self.clean("No"))

    def test_clean_true(self):
        self.assertTrue(self.clean(True))
