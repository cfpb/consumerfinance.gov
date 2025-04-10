from django.test import TestCase

from searchgov.forms import SearchForm


class SearchFormTestCase(TestCase):
    def test_clean_term(self):
        form = SearchForm(data={"q": "    payday^~`[]#<>;|%\\{\\}\\"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["q"], "payday")
        self.assertEqual(1, form.cleaned_data["page"])

    def test_clean_page(self):
        form = SearchForm(data={"q": "payday", "page": 3})
        self.assertTrue(form.is_valid())
        self.assertEqual(3, form.cleaned_data["page"])

        form = SearchForm(data={"q": "payday", "page": "4"})
        self.assertTrue(form.is_valid())
        self.assertEqual(4, form.cleaned_data["page"])

    def test_invalid_page(self):
        form = SearchForm(data={"q": "payday", "page": "fake"})
        self.assertFalse(form.is_valid())
