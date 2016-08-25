from django.test import TestCase
from v1.models.base import CFGOVPage
from mock import patch

class TestAuthorNames(TestCase):

    def test_authors_get_sorted_alphabetically_by_default(self): 
        with patch.object(CFGOVPage, 'alphabetize_authors') as mock:
            CFGOVPage().get_authors()
        mock.assert_called_with()

    def test_alphabetize_authors_by_last_name(self):
        page = CFGOVPage()
        page.authors.add('Ross Karchner','Richa Agarwal', 'Andy Chosak', 'Will Barton')
        expected_result = ['Richa Agarwal', 'Will Barton', 'Andy Chosak', 'Ross Karchner']
        self.assertEquals(page.alphabetize_authors(), expected_result)
    
    def test_no_authors(self):
        page = CFGOVPage()
        self.assertEquals(page.alphabetize_authors(), [])

    def test_author_with_middle_name(self):
        page = CFGOVPage()
        page.authors.add('Jess Schafer', 'Richa Something Agarwal', 'Sarah Simpson')
        expected_result = ['Richa Something Agarwal', 'Jess Schafer', 'Sarah Simpson']
        self.assertEquals(page.alphabetize_authors(), expected_result)


if __name__ == '__main__':
    unittest.main()

