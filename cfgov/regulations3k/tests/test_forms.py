from django.test import TestCase

from regulations3k.forms import RegDownField, RegDownTextarea


class RegDownFieldTestCase(TestCase):

    def test_widget(self):
        f = RegDownField()
        self.assertEqual(type(f.widget), RegDownTextarea)
