import os.path

from django.test import SimpleTestCase

from tccp.dataset import (
    convert_header_to_field_name,
    read_survey_data_from_stream,
)


class ConvertHeaderToFieldNameTests(SimpleTestCase):
    def check_conversion(self, header, field_name):
        self.assertEqual(convert_header_to_field_name(header), field_name)

    def test_conversion(self):
        self.check_conversion("Some column", "some_column")
        self.check_conversion("Some column ($)", "some_column_dollars")
        self.check_conversion("Some column (%)", "some_column_percentage")
        self.check_conversion("A-column-with-dashes", "a_column_with_dashes")


class ReadSurveyDataFromStreamTests(SimpleTestCase):
    def test_load_from_filename(self):
        filename = os.path.join(
            os.path.dirname(__file__), "data", "sample.xlsx"
        )
        with open(filename, "rb") as f:
            dataset = read_survey_data_from_stream(f)

        self.assertEqual(len(dataset), 5)
        self.assertEqual(dataset[0]["institution_name"], "SAMPLE BANK")
