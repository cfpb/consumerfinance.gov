from django import forms
from django.http import HttpResponseRedirect
from django.test import RequestFactory, TestCase

from data_research.handlers import ConferenceRegistrationHandler


class MockConferenceRegistrationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.pop("capacity")
        kwargs.pop("govdelivery_code")
        kwargs.pop("govdelivery_question_id")
        kwargs.pop("govdelivery_answer_id")
        super().__init__(*args, **kwargs)

    def save(self, commit=False):
        pass

    @property
    def at_capacity(self):
        return False


class AtCapacityConferenceRegistrationForm(MockConferenceRegistrationForm):
    @property
    def at_capacity(self):
        return True


class ExceptionThrowingConferenceRegistrationForm(MockConferenceRegistrationForm):
    def save(self, commit=False):
        raise RuntimeError("something went wrong")


class TestConferenceRegistrationHandler(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.path = "/path/to/form"
        self.page = object()

        self.block_value = {
            "capacity": "100",
            "govdelivery_code": "ABC123",
            "govdelivery_question_id": "12345",
            "govdelivery_answer_id": "67890",
            "failure_message": "Something went wrong in a test.",
        }

    def get_handler(self, request=None, form_cls=None):
        if request is None:
            request = self.factory.post(self.path)

        if form_cls is None:
            form_cls = MockConferenceRegistrationForm

        return ConferenceRegistrationHandler(
            page=self.page,
            request=request,
            block_value=self.block_value,
            form_cls=form_cls,
        )

    def test_process_not_submitted_returns_empty_form(self):
        response = self.get_handler().process(is_submitted=False)
        self.assertFalse(response["form"].is_bound)

    def test_process_not_at_capacity(self):
        response = self.get_handler().process(is_submitted=False)
        self.assertFalse(response["is_at_capacity"])

    def test_process_at_capacity(self):
        handler = self.get_handler(form_cls=AtCapacityConferenceRegistrationForm)
        response = handler.process(is_submitted=False)
        self.assertTrue(response["is_at_capacity"])

    def test_process_not_submitted_not_successful_submission(self):
        response = self.get_handler().process(is_submitted=False)
        self.assertFalse(response["is_successful_submission"])

    def test_request_with_query_string_marks_successful_submission(self):
        request = self.factory.get("/?success")
        handler = self.get_handler(request=request)
        response = handler.process(is_submitted=False)
        self.assertTrue(response["is_successful_submission"])

    def test_successful_process_returns_redirect(self):
        response = self.get_handler().process(is_submitted=True)
        self.assertIsInstance(response, HttpResponseRedirect)

    def test_successful_process_returns_temporary_redirect(self):
        response = self.get_handler().process(is_submitted=True)
        self.assertEqual(response.status_code, 302)

    def test_process_returns_redirect_with_query_string_parameter(self):
        response = self.get_handler().process(is_submitted=True)
        self.assertEqual(response["Location"], self.path + "?success")

    def test_process_exception_sets_form_error(self):
        handler = self.get_handler(form_cls=ExceptionThrowingConferenceRegistrationForm)
        response = handler.process(is_submitted=True)
        self.assertEqual(
            response["form"].non_field_errors(),
            ["Something went wrong in a test."],
        )
