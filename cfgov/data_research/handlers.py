from __future__ import absolute_import, unicode_literals

import logging

from django.http import HttpResponseRedirect

from data_research.forms import ConferenceRegistrationForm
from data_research.models import ConferenceRegistration
from v1.handlers import Handler


logger = logging.getLogger(__name__)


class ConferenceRegistrationHandler(Handler):
    SUCCESS_QUERY_STRING_PARAMETER = 'success'
    """Query string parameter that gets set on successful form submission.

    This parameter gets set in the redirect URL that gets returned after
    the conference registration form is successfully submitted.
    """

    def __init__(self, page, request, block_value, form_cls=None):
        super(ConferenceRegistrationHandler, self).__init__(page, request)
        self.govdelivery_code = block_value['govdelivery_code']
        self.capacity = block_value['capacity']
        self.failure_message = block_value['failure_message']
        self.form_cls = form_cls or ConferenceRegistrationForm

    def process(self, is_submitted):
        is_at_capacity = self._is_at_capacity()
        is_successful_submission = self._is_successful_submission()

        # If the form was submitted, and there's still room in the conference,
        # and this isn't being processed as part of the response after a
        # successful submission, go ahead with the registration flow.
        if (
            is_submitted and
            not is_at_capacity and
            not is_successful_submission
        ):
            form = self.form_cls(
                govdelivery_code=self.govdelivery_code,
                data=self.request.POST
            )

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
            form = self.form_cls(govdelivery_code=self.govdelivery_code)

        return {
            'form': form,
            'is_at_capacity': is_at_capacity,
            'is_successful_submission': is_successful_submission,
        }

    def _is_at_capacity(self):
        attendees = ConferenceRegistration.objects.filter(
            govdelivery_code=self.govdelivery_code
        )
        return attendees.count() >= self.capacity

    def _is_successful_submission(self):
        return self.SUCCESS_QUERY_STRING_PARAMETER in self.request.GET
