from django.core import mail
from django.test import TestCase
from django.urls import reverse


class TestGetAssessmentForm(TestCase):
    def test_invalid_form_post_does_not_send_email(self):
        self.client.post(
            reverse("diversity_inclusion:voluntary_assessment_form"),
            {
                "institution_name": "Institution Name",
                "institution_address": "123 Main Street",
                "institution_city": "Anytown",
                "institution_state": "NA",
                "institution_zip": "12345",
                "tax_id": "123456789",
                "contact_name": "Human Being",
                "contact_title": "Job Title",
                "contact_email": "Not a valid email address",
                "contact_phone": "(123) 456-7890",
                "contact_phone_alt": "",
            },
        )

        self.assertEqual(len(mail.outbox), 0)

    def test_valid_form_post_sends_email_and_redirects(self):
        response = self.client.post(
            reverse("diversity_inclusion:voluntary_assessment_form"),
            {
                "institution_name": "Institution Name",
                "institution_address": "123 Main Street",
                "institution_city": "Anytown",
                "institution_state": "NA",
                "institution_zip": "12345",
                "tax_id": "123456789",
                "contact_name": "Human Being",
                "contact_title": "Job Title",
                "contact_email": "human.being@institution.name",
                "contact_phone": "(123) 456-7890",
                "contact_phone_alt": "",
            },
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject,
            "Diversity assessment submission from Institution Name",
        )
        self.assertEqual(
            mail.outbox[0].to, ["OMWI_diversityassessments@cfpb.gov"]
        )
        self.assertRedirects(
            response, reverse("diversity_inclusion:form_submitted")
        )
