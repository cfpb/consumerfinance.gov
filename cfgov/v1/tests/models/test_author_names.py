from django.test import TestCase

from v1.models.base import CFGOVPage


class TestAuthorNames(TestCase):
    def check_authors(self, authors, expected):
        page = CFGOVPage()
        page.authors.add(*authors)
        self.assertEqual(page.get_authors(), expected)

    def test_author_names_with_no_space(self):
        self.check_authors(
            ["Wyatt Pearsall", "CFPB"], ["CFPB", "Wyatt Pearsall"]
        )

    def test_alphabetize_authors_by_last_name(self):
        self.check_authors(
            ["Ross Karchner", "Richa Agarwal", "Andy Chosak", "Will Barton"],
            ["Richa Agarwal", "Will Barton", "Andy Chosak", "Ross Karchner"],
        )

    def test_no_authors(self):
        self.check_authors([], [])

    def test_author_with_middle_name(self):
        self.check_authors(
            ["Jess Schafer", "Richa Something Agarwal", "Sarah Simpson"],
            [
                "Richa Something Agarwal",
                "Jess Schafer",
                "Sarah Simpson",
            ],
        )

    def test_same_last_names(self):
        self.check_authors(
            ["Mary Smith", "Vic Kumar", "John Smith"],
            ["Vic Kumar", "John Smith", "Mary Smith"],
        )
