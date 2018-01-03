from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings

import mock


@override_settings(FLAGS={'SEARCH_DOTGOV_API': {'boolean': 'True'}})
class SearchViewsTestCase(TestCase):

    @mock.patch('search.dotgov.search')
    def test_results_view(self, mock_search):
        mock_search.return_value = {'web': {'results': []}}
        response = self.client.get(reverse('search_results'), {'q': 'auto'})
        mock_search.assert_called()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['q'], 'auto')
        self.assertEqual(response.context_data['results'],
                         {'web': {'results': []}})
