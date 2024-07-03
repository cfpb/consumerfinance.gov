from datetime import date
from unittest.mock import MagicMock, patch

from django import forms
from django.test import SimpleTestCase, TestCase

from wagtail.images.forms import get_image_form

from freezegun import freeze_time

from v1.forms import FilterableDateField, FilterableListForm
from v1.models import CFGOVImage


class TestFilterableListFormDateFields(SimpleTestCase):
    def check_date_fields(self, data, expected_from_date, expected_to_date):
        form = FilterableListForm(filterable_search=MagicMock(), data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["from_date"], expected_from_date)
        self.assertEqual(form.cleaned_data["to_date"], expected_to_date)

    @freeze_time("2020-01-01")
    def test_clean_returns_cleaned_data_if_in_future(self):
        self.check_date_fields(
            data={
                "from_date": "2048-01-23",
                "to_date": "2049-01-23",
            },
            expected_from_date=date(2048, 1, 23),
            expected_to_date=date(2049, 1, 23),
        )

    def test_clean_returns_cleaned_data_if_valid(self):
        self.check_date_fields(
            data={
                "from_date": "2017-07-04",
                "to_date": "2017-07-05",
            },
            expected_from_date=date(2017, 7, 4),
            expected_to_date=date(2017, 7, 5),
        )

    @patch(
        "v1.forms.FilterableListForm.first_page_date",
        return_value=date(1995, 1, 1),
    )
    def test_clean_uses_earliest_result_if_fromdate_field_is_empty(self, _):
        self.check_date_fields(
            data={"to_date": "2017-01-15"},
            expected_from_date=date(1995, 1, 1),
            expected_to_date=date(2017, 1, 15),
        )

    @freeze_time("2020-01-01")
    def test_clean_uses_today_if_todate_field_is_empty(self):
        self.check_date_fields(
            data={"from_date": "2016-05-15"},
            expected_from_date=date(2016, 5, 15),
            expected_to_date=date(2020, 1, 1),
        )

    def test_clean_returns_cleaned_data_if_both_date_fields_are_empty(self):
        self.check_date_fields(
            data={},
            expected_from_date=None,
            expected_to_date=None,
        )

    def test_clean_switches_date_fields_if_todate_is_less_than_fromdate(self):
        self.check_date_fields(
            data={
                "from_date": "2017-07-05",
                "to_date": "2017-07-04",
            },
            expected_from_date=date(2017, 7, 4),
            expected_to_date=date(2017, 7, 5),
        )


class TestFilterableDateField(SimpleTestCase):
    def test_default_required(self):
        field = FilterableDateField()
        self.assertFalse(field.required)

    def test_set_required(self):
        field = FilterableDateField(required=True)
        self.assertTrue(field.required)


class CFGOVImageFormTests(TestCase):
    def test_alt_widget_override(self):
        form_cls = get_image_form(CFGOVImage)
        form = form_cls()
        self.assertIsInstance(form.fields["alt"].widget, forms.TextInput)
