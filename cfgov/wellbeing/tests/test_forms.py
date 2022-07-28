from django.test import TestCase

from wellbeing.forms import FWBScore, ResultsForm


class TestFWBScore(TestCase):
    def test_return_score(self):
        self.assertEqual(FWBScore(47).score, 47)
        self.assertEqual(str(FWBScore(47)), "47")

    def test_avg(self):
        self.assertEqual(FWBScore.avg().score, FWBScore.AVG)

    def test_pct_low(self):
        self.assertEqual(FWBScore(14).pct, 0)

    def test_pct_mid(self):
        self.assertAlmostEqual(FWBScore(54).pct, 49.382716049382715)

    def test_pct_high(self):
        self.assertEqual(FWBScore(95).pct, 100)

    def test_return_color_group_1(self):
        self.assertEqual(FWBScore(14).color, "#e05f21")
        self.assertEqual(FWBScore(39).color, "#e05f21")

    def test_return_color_group_2(self):
        self.assertEqual(FWBScore(40).color, "#f9921c")
        self.assertEqual(FWBScore(49).color, "#f9921c")

    def test_return_color_group_3(self):
        self.assertEqual(FWBScore(50).color, "#a6a329")
        self.assertEqual(FWBScore(59).color, "#a6a329")

    def test_return_color_group_4(self):
        self.assertEqual(FWBScore(60).color, "#44a839")
        self.assertEqual(FWBScore(69).color, "#44a839")

    def test_return_color_group_5(self):
        self.assertEqual(FWBScore(70).color, "#398c7a")
        self.assertEqual(FWBScore(95).color, "#398c7a")


class TestResultsForm(TestCase):
    def test_empty_data_is_invalid(self):
        post_data = {}

        form = ResultsForm(post_data)
        self.assertFalse(form.is_valid())

    def test_partial_data_is_invalid(self):
        post_data = {
            # not all data is filled out
            "question_1": "4",
        }

        form = ResultsForm(post_data)
        self.assertFalse(form.is_valid())

    def test_wrong_kind_of_data_is_invalid(self):
        post_data = {
            # data is in the wrong format to get a score back
            "question_1": "abc",
            "question_2": "def",
            "question_3": "ghi",
            "question_4": "jkl",
            "question_5": "mno",
            "question_6": "pqr",
            "question_7": "stu",
            "question_8": "vwx",
            "question_9": "y",
            "question_10": "z",
            "age": "62-plus",
            "method": "read-self",
        }

        form = ResultsForm(post_data)
        self.assertFalse(form.is_valid())

    def test_correct_data_returns_score_and_answers(self):
        post_data = {
            "question_1": "4",
            "question_2": "3",
            "question_3": "2",
            "question_4": "1",
            "question_5": "4",
            "question_6": "3",
            "question_7": "2",
            "question_8": "3",
            "question_9": "0",
            "question_10": "1",
            "age": "62-plus",
            "method": "read-self",
        }

        form = ResultsForm(post_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["user_score"].score, 57)
