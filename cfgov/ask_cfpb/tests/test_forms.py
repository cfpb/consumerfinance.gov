from django.test import TestCase

from ask_cfpb.forms import AutocompleteForm, SearchForm


class AutocompleteFormTestCase(TestCase):
    def test_clean_term(self):
        form = AutocompleteForm(data={'term': '    payday^~`[]#<>;|%\\{\\}\\'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['term'], 'payday')


class SearchFormTestCase(TestCase):
    def test_clean_term(self):
        form = SearchForm(data={'q': '    payday^~`[]#<>;|%\\{\\}\\'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['q'], 'payday')

    def test_clean_correct(self):
        form = SearchForm(data={'q': 'payday'})
        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data['correct'])

        form = SearchForm(data={'q': 'payday', 'correct': '1'})
        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data['correct'])

        form = SearchForm(data={'q': 'payday', 'correct': '0'})
        self.assertTrue(form.is_valid())
        self.assertFalse(form.cleaned_data['correct'])
