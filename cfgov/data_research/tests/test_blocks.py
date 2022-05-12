from django.core.exceptions import ValidationError
from django.test import TestCase

from data_research.blocks import ConferenceRegistrationForm
from v1.models import BrowsePage


class ConferenceRegistrationFormTests(TestCase):
    fixtures = ["conference_registration_page.json"]

    def test_page_renders_using_template(self):
        page = BrowsePage.objects.get(pk=99999)
        request = self.client.get("/").wsgi_request
        response = page.serve(request)
        self.assertContains(response, "other accommodations needed to attend?")


class TestConfRegFormBlockValidation(TestCase):
    def test_conf_reg_block_without_question_or_answer_passes_validation(self):
        block = ConferenceRegistrationForm()
        value = block.to_python(
            {
                "govdelivery_code": "USCFPB_999",
                "capacity": 123,
                "success_message": "Success message",
                "at_capacity_message": "At capacity message",
                "failure_message": "Failure message",
            }
        )
        self.assertTrue(block.clean(value))

    def test_conf_reg_block_with_question_but_no_answer_fails_validation(self):
        block = ConferenceRegistrationForm()
        value = block.to_python(
            {
                "govdelivery_code": "USCFPB_999",
                "govdelivery_question_id": "12345",
                "govdelivery_answer_id": "",
                "capacity": 123,
                "success_message": "Success message",
                "at_capacity_message": "At capacity message",
                "failure_message": "Failure message",
            }
        )

        with self.assertRaises(ValidationError):
            block.clean(value)

    def test_conf_reg_block_with_answer_but_no_question_fails_validation(self):
        block = ConferenceRegistrationForm()
        value = block.to_python(
            {
                "govdelivery_code": "USCFPB_999",
                "govdelivery_question_id": "",
                "govdelivery_answer_id": "67890",
                "capacity": 123,
                "success_message": "Success message",
                "at_capacity_message": "At capacity message",
                "failure_message": "Failure message",
            }
        )

        with self.assertRaises(ValidationError):
            block.clean(value)

    def test_conf_reg_block_with_answer_and_question_passes_validation(self):
        block = ConferenceRegistrationForm()
        value = block.to_python(
            {
                "govdelivery_code": "USCFPB_999",
                "govdelivery_question_id": "12345",
                "govdelivery_answer_id": "67890",
                "capacity": 123,
                "success_message": "Success message",
                "at_capacity_message": "At capacity message",
                "failure_message": "Failure message",
            }
        )
        self.assertTrue(block.clean(value))
