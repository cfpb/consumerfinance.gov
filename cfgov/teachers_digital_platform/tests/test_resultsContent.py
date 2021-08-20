from django.test import TestCase

from ..resultsContent import ResultsContent, _results_data_row


class ResultsContentTest(TestCase):

    def setUp(self):
        self.ResultsContent = ''

    def test_results_data_row(self):
        row = {'Key': 'test_key1', 'Content': 'test_value1'}
        test_array = _results_data_row(row)
        self.assertEqual(test_array, {'k': 'test_key1', 'v': 'test_value1'})

    def test_factory_elementary_school(self):
        rc = ResultsContent.factory('3-5')
        self.assertIsInstance(rc, ResultsContent)
        self.assertEqual(rc.store['BB0'], 'Planning and self-control')
        self.assertEqual(rc.key, '3-5')

    def test_factory_middle_school(self):
        rc = ResultsContent.factory('6-8')
        self.assertIsInstance(rc, ResultsContent)
        self.assertEqual(rc.store['BB0'], 'Planning and self-control')
        self.assertEqual(rc.key, '6-8')

    def test_factory_high_school(self):
        rc = ResultsContent.factory('9-12')
        self.assertIsInstance(rc, ResultsContent)
        self.assertEqual(rc.store['BB0'], 'Planning and self-control')
        self.assertEqual(rc.key, '9-12')
