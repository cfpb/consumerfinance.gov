from django.test import TestCase

from paying_for_college.validators import (
    clean_boolean,
    clean_float,
    clean_integer,
    clean_string,
    clean_yes_no,
)


class ValidatorTestCase(TestCase):
    def test_clean_integer(self):
        self.assertTrue(clean_integer(1) == 1)
        self.assertTrue(clean_integer(1.1) == 1)
        self.assertTrue(clean_integer(0) == 0)
        self.assertTrue(clean_integer("c") == 0)
        self.assertTrue(clean_integer(None) == 0)

    def test_clean_float(self):
        self.assertTrue(clean_float(0.1) == 0.1)
        self.assertTrue(clean_float(1) == 1.0)
        self.assertTrue(clean_float("c") == 0)
        self.assertTrue(clean_float(None) == 0)

    def test_clean_string(self):
        self.assertTrue(clean_string("test") == "test")
        self.assertTrue(clean_string("<test>") == "test")
        self.assertTrue(clean_string(0) == "")
        self.assertTrue(clean_string(10) == "")
        self.assertTrue(clean_string("") == "")

    def test_clean_boolean(self):
        self.assertFalse(clean_boolean("False"))
        self.assertFalse(clean_boolean("false"))
        self.assertFalse(clean_boolean("0"))
        self.assertTrue(clean_boolean("True"))
        self.assertTrue(clean_boolean("true"))
        self.assertTrue(clean_boolean("1"))
        self.assertTrue(clean_boolean("") == "")
        self.assertTrue(clean_boolean("test") == "")

    def test_clean_yes_no(self):
        self.assertTrue(clean_yes_no("no") == "No")
        self.assertTrue(clean_yes_no("yes") == "Yes")
        self.assertTrue(clean_yes_no("") == "")
        self.assertTrue(clean_yes_no("anything else") == "")
