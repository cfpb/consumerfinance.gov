from unittest import mock

from django.test import TestCase

from search.dotgov import search, typeahead


class SearchDotGovTestCase(TestCase):

    @mock.patch('search.dotgov.requests.get')
    def test_search_query(self, mock_get):
        mock_get.return_value.ok = True
        search('query')
        mock_get.return_value.json.assert_called()

    @mock.patch('search.dotgov.requests.get')
    def test_search_query_bad_upstream_response(self, mock_get):
        mock_get.return_value.ok = False
        result = search('')
        self.assertEqual(result, {})

    def test_search_limit_out_of_bounds(self):
        with self.assertRaises(ValueError):
            search('query', limit=0)

        with self.assertRaises(ValueError):
            search('query', limit=51)

    def test_search_offset_out_of_bounds(self):
        with self.assertRaises(ValueError):
            search('query', offset=-1)

        with self.assertRaises(ValueError):
            search('query', offset=1000)

    def test_search_sort_by_out_of_bounds(self):
        with self.assertRaises(ValueError):
            search('query', sort_by='alpha')

    @mock.patch('search.dotgov.requests.get')
    def test_typeahead(self, mock_get):
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = ['auto']
        result = typeahead('au')
        self.assertEqual(result, ['auto'])

    @mock.patch('search.dotgov.requests.get')
    def test_typeahead_bad_upstream_response(self, mock_get):
        mock_get.return_value.ok = False
        result = typeahead('')
        self.assertEqual(result, [])
