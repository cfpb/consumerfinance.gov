import json
import logging

from django.conf import settings
from django.core.exceptions import NON_FIELD_ERRORS
from django.http import HttpResponseRedirect

from govdelivery.api import GovDelivery

from data_research.forms import ConferenceRegistrationForm
from data_research.models import ConferenceRegistration
from v1.handlers import Handler


logger = logging.getLogger(__name__)


class ConferenceRegistrationHandler(Handler):
    SUCCESS_QUERY_STRING_PARAMETER = 'success'

    def __init__(self, page, request, block_value):
        super(ConferenceRegistrationHandler, self).__init__(page, request)
        self.block_value = block_value

    def process(self, is_submitted):
        if self.is_at_capacity():
            return {'is_at_capacity': True}

        if is_submitted:
            data = self.get_post_data()
            form = ConferenceRegistrationForm(data)

            if form.is_valid():
                attendee = form.save(commit=False)

                if self.subscribe(attendee.email, attendee.code):
                    attendee.save()
                    return HttpResponseRedirect(self.success_url)

                form.add_error(
                    NON_FIELD_ERRORS,
                    self.block_value['failure_message']
                )

            return {'form': form}

        return {
            'form': ConferenceRegistrationForm(),
            'is_successful_submission': self.is_successful_submission(),
        }

    def is_at_capacity(self):
        capacity = self.block_value['capacity']
        code = self.block_value['code']

        attendees = ConferenceRegistration.objects.filter(code=code)
        return attendees.count() >= capacity

    def is_successful_submission(self):
        return self.SUCCESS_QUERY_STRING_PARAMETER in self.request.GET

    def get_post_data(self):
        data = self.request.POST.copy()

        sessions = self.get_sessions()
        data['sessions'] = json.dumps(sessions) if sessions else ''

        return data

    def get_sessions(self):
        ids = self.request.POST.getlist('form_sessions', [])
        sessions = self.block_value.get('sessions', [])
        return [session for i, session in enumerate(sessions) if str(i) in ids]

    def subscribe(self, email, code):
        try:
            logger.info('subscribing to GovDelivery')
            gd = GovDelivery(account_code=settings.ACCOUNT_CODE)

            subscription_response = gd.set_subscriber_topics(
                email_address=email,
                topic_codes=[code],
                send_notifications=True,
            )

            subscription_response.raise_for_status()
        except Exception:
            logger.exception('error subscribing to GovDelivery')
            return False

        return True

    @property
    def success_url(self):
        return '{}?{}'.format(
            self.request.path,
            self.SUCCESS_QUERY_STRING_PARAMETER
        )
