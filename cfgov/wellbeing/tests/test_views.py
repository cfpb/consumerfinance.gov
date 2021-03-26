from django.test import TestCase
from django.urls import reverse


class TestTemplatesAsViews(TestCase):
    def test_home_template(self):
        response = self.client.get(reverse('fwb_home_en'))
        self.assertEqual(response.status_code, 200)

    def test_about_template(self):
        response = self.client.get(reverse('fwb_about_en'))
        self.assertEqual(response.status_code, 200)


class TestResultsView(TestCase):
    def test_results_view_get(self):
        response = self.client.get(reverse('fwb_results_en'))
        self.assertContains(response, 'If you would like to see your score')

    def test_results_view_post_invalid(self):
        response = self.client.post(
            reverse('fwb_results_en'),
            {
                # not all fields are filled out
                "question_1": "4",
            },
        )
        self.assertContains(
            response,
            "There was a problem with your submission",
            status_code=400,
        )

    def test_results_view_post_successful(self):
        response = self.client.post(
            reverse('fwb_results_en'),
            {
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
            },
        )
        self.assertContains(
            response, 'Your score: <b class="score-value">57</b>'
        )
