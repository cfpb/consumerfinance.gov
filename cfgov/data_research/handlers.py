import logging

from django.http import HttpResponseRedirect

from data_research.forms import ConferenceRegistrationForm
from v1.handlers import Handler


logger = logging.getLogger(__name__)


class ConferenceRegistrationHandler(Handler):
    SUCCESS_QUERY_STRING_PARAMETER = 'success'
    """Query string parameter that gets set on successful form submission.

    This parameter gets set in the redirect URL that gets returned after
    the conference registration form is successfully submitted.
    """

    def __init__(self, page, request, block_value, form_cls=None):
        super().__init__(page, request)
        self.govdelivery_code = block_value['govdelivery_code']
        self.govdelivery_question_id = block_value['govdelivery_question_id']
        self.govdelivery_answer_id = block_value['govdelivery_answer_id']
        self.capacity = block_value['capacity']
        self.failure_message = block_value['failure_message']
        self.form_cls = form_cls or ConferenceRegistrationForm

    def process(self, is_submitted):
        is_successful_submission = self._is_successful_submission()

        form_kwargs = {
            'capacity': self.capacity,
            'govdelivery_code': self.govdelivery_code,
            'govdelivery_question_id': self.govdelivery_question_id,
            'govdelivery_answer_id': self.govdelivery_answer_id
        }

        # If the form was submitted, and there's still room in the conference,
        # and this isn't being processed as part of the response after a
        # successful submission, go ahead with the registration flow.
        if (
            is_submitted and
            not is_successful_submission
        ):
            form = self.form_cls(data=self.request.POST, **form_kwargs)

            try:
                if form.is_valid():
                    form.save()

                    return HttpResponseRedirect('{}?{}'.format(
                        self.request.path,
                        self.SUCCESS_QUERY_STRING_PARAMETER
                    ))
            except Exception:
                logger.exception("conference registration form error")
                form.add_error(None, self.failure_message)
        else:
            form = self.form_cls(**form_kwargs)

        return {
            'form': form,
            'is_at_capacity': form.at_capacity,
            'is_successful_submission': is_successful_submission,
        }

    def _is_successful_submission(self):
        return self.SUCCESS_QUERY_STRING_PARAMETER in self.request.GET
