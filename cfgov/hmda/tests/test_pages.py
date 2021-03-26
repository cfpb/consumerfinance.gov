from django.test import RequestFactory, TestCase

from model_bakery import baker

from hmda.models.pages import HmdaHistoricDataPage


class TestHmdaHistoricDataPage(TestCase):
    expected_years = ['2017', '2016', '2015', '2014', '2013', '2012',
                      '2011', '2010', '2009', '2008', '2007']

    def setUp(self):
        self.factory = RequestFactory()

    def test_hmda_explorer_page_no_params(self):
        page = baker.prepare(HmdaHistoricDataPage)
        test_context = page.get_context(self.factory.get('/'))

        self.assertEqual(test_context['title'], 'Showing nationwide records')
        self.assertEqual(
            test_context['subtitle'],
            'Mortgages for first lien, owner-occupied, 1-4 family homes')
        years = [item[0] for item in test_context['files']]
        self.assertEqual(years, self.expected_years)

    def test_hmda_explorer_page_with_params(self):
        page = baker.prepare(HmdaHistoricDataPage)
        request = '/?geo=ny&records=all-records&field_descriptions=codes'
        test_context = page.get_context(self.factory.get(request))

        self.assertEqual(test_context['title'], 'Showing records for New York')
        self.assertEqual(test_context['subtitle'], 'All records')
        years = [item[0] for item in test_context['files']]
        self.assertEqual(years, self.expected_years)
