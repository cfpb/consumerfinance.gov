from django.test import TestCase

from regulations3k.forms import RegDownField
from regulations3k.models.fields import RegDownTextField


class RegDownTextFieldTests(TestCase):

    def test_formfield(self):
        regdown_field = RegDownTextField()
        form_field = regdown_field.formfield()
        self.assertEqual(type(form_field), RegDownField)
