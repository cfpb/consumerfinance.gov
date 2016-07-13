from unittest import TestCase

from v1.forms import ActivityLogFilterForm
from v1.models.sublanding_filterable_page import ActivityLogPage


class ActivityLogPageTestCase(TestCase):
    def test_get_form_class(self):
        self.assertEqual(
            ActivityLogPage.get_form_class(),
            ActivityLogFilterForm
        )
