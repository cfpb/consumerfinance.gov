from django.db import IntegrityError
from django.test import TestCase

from mega_menu.models import Menu


class MenuTests(TestCase):
    def test_str(self):
        self.assertEqual(str(Menu("en")), "English")
        self.assertEqual(str(Menu("es")), "Spanish")

    def test_unique_for_language(self):
        Menu.objects.create(language="en")
        with self.assertRaises(IntegrityError):
            Menu.objects.create(language="en")
