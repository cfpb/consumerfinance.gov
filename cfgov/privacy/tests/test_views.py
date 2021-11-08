from django.core import mail
from django.test import TestCase
from django.urls import reverse


class TestGetAssessmentForm(TestCase):
    # def test_invalid_form_post_does_not_send_email(self):
    #     self.client.post(
    #         reverse("foia:foia_form"),
    #         {
    #             "subject_line": "",
    #         },
    #     )

    #     self.assertEqual(len(mail.outbox), 0)

    # def test_valid_form_post_sends_email_and_redirects(self):
    #     response = self.client.post(
    #         reverse("diversity_inclusion:voluntary_assessment_form"),
    #         {
    #             "subject_line": "something",
    #         },
    #     )

    #     self.assertEqual(len(mail.outbox), 1)
    #     self.assertEqual(
    #         mail.outbox[0].subject,
    #         "Online FOIA request: something",
    #     )
    #     self.assertEqual(
    #         mail.outbox[0].to, ["elizabeth.lorton@cfpb.gov"]
    #     )
    #     self.assertRedirects(
    #         response, reverse("foia:foia_form_submitted")
    #     )
