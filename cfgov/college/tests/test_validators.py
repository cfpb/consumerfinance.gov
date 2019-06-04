from django.core.exceptions import ValidationError
from django.test import TestCase

from college.validators import (
    clean_boolean, clean_float, clean_integer, clean_string, clean_yes_no,
    validate_uuid4
)


INVALID_UUID = """
\r\n\r\nOMG CHECK OUT THIS TOTES LEGIT CFPB-APPROVED WEBSITE: /
http://nyan.cat\r\n\r\nOh, and here is some Kafka:\r\n\r\nOne morning, /
as Gregor Samsa was waking up from anxious dreams, /
he discovered that in his bed he had been changed into a monstrous /
verminous bug. He lay on his armour-hard back and saw, as he lifted /
his head up a little, his brown, arched abdomen divided up into rigid /
bow-like sections. From this height the blanket, just about ready /
to slide off completely, could hardly stay in place. His numerous legs, /
pitifully thin in comparison to the rest of his circumference, /
flickered helplessly before his eyes.\r\n
"""

VALID_WORKSHEET_DATA = """{"1": \
{"school":"University of Kansas",\
"alias":"Jayhawks",\
"netpriceok":500,\
"control":"Public",\
"oncampusavail":"Yes",\
"tuitiongradoss":"",\
"offerba":"Yes",\
"state":"KS",\
"books":500,\
"online":"No",\
"school_id":"155317"}}
"""

INVALID_WORKSHEET_DATA = """{"1": {"school": \
"University of Kansas | Jayhawks'}}
"""

DIRTY_WORKSHEET_DATA = """{"1": {"school": \
"<script>console.log('INVALID');</script>"}}
"""


class UUIDValidatorTestCase(TestCase):
    def test_valid_uuid4(self):
        result = validate_uuid4('841df17e-784f-4ea4-bfb3-ebac5d2fcfe5')
        # UUID validator does not return a value, only indications are raising
        # ValidationError, or not
        self.assertEqual(result, None)

    def test_invalid_uuid4(self):
        self.assertRaises(ValidationError, validate_uuid4, INVALID_UUID)


class WorkSheetValidatorTestCase(TestCase):

    # def test_valid_worksheet_data(self):
    #     result = validate_worksheet(VALID_WORKSHEET_DATA)
    #     self.assertTrue('Jayhawks' in result)

    # def test_invalid_worksheet_data(self):
    #     self.assertRaises(ValidationError,
    #                       validate_worksheet,
    #                       INVALID_WORKSHEET_DATA)

    # def test_dirty_worksheet_data(self):
    #     result = validate_worksheet(DIRTY_WORKSHEET_DATA)
    #     self.assertFalse('<' in result)

    def test_clean_integer(self):
        self.assertTrue(clean_integer(1) == 1)
        self.assertTrue(clean_integer(1.1) == 1)
        self.assertTrue(clean_integer(0) == 0)
        self.assertTrue(clean_integer('c') == 0)
        self.assertTrue(clean_integer(None) == 0)

    def test_clean_float(self):
        self.assertTrue(clean_float(0.1) == 0.1)
        self.assertTrue(clean_float(1) == 1.0)
        self.assertTrue(clean_float('c') == 0)
        self.assertTrue(clean_float(None) == 0)

    def test_clean_string(self):
        self.assertTrue(clean_string("test") == "test")
        self.assertTrue(clean_string("<test>") == "test")
        self.assertTrue(clean_string(0) == "")
        self.assertTrue(clean_string(10) == "")
        self.assertTrue(clean_string("") == "")

    def test_clean_boolean(self):
        self.assertFalse(clean_boolean('False'))
        self.assertFalse(clean_boolean('false'))
        self.assertFalse(clean_boolean('0'))
        self.assertTrue(clean_boolean('True'))
        self.assertTrue(clean_boolean('true'))
        self.assertTrue(clean_boolean('1'))
        self.assertTrue(clean_boolean('') == "")
        self.assertTrue(clean_boolean('test') == "")

    def test_clean_yes_no(self):
        self.assertTrue(clean_yes_no('no') == 'No')
        self.assertTrue(clean_yes_no('yes') == 'Yes')
        self.assertTrue(clean_yes_no('') == '')
        self.assertTrue(clean_yes_no('anything else') == '')
