import json
import logging

from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from govdelivery.api import GovDelivery

from data_research.forms import ConferenceRegistrationForm
from data_research.models import ConferenceRegistration
from v1.handlers import Handler


logger = logging.getLogger(__name__)


class ConferenceRegistrationHandler(Handler):
    def __init__(self, page, request, block_value):
        super(ConferenceRegistrationHandler, self).__init__(page, request)
        self.block_value = block_value

    def process(self, is_submitted):
        if self.is_at_capacity():
            return {
                'form': ConferenceRegistrationForm(),
                'is_at_capacity': True
            }

        if is_submitted:
            data = self.get_post_data()
            form = ConferenceRegistrationForm(data)
            return self.get_response(form)

        return {'form': ConferenceRegistrationForm()}

    def is_at_capacity(self):
        capacity = self.block_value['capacity']
        code = self.block_value['code']

        attendees = ConferenceRegistration.objects.filter(code=code)
        return attendees.count() >= capacity

    def get_post_data(self):
        data = self.request.POST.copy()

        sessions = self.get_sessions()
        data['sessions'] = json.dumps(sessions) if sessions else ''

        return data

    def get_sessions(self):
        ids = self.request.POST.getlist('form_sessions', [])
        sessions = self.block_value.get('sessions', [])
        return [session for i, session in enumerate(sessions) if str(i) in ids]

    def get_response(self, form):
        if form.is_valid():
            attendee = form.save(commit=False)

            if self.subscribe(attendee.email, attendee.code):
                attendee.save()
                return self.success()

        return self.fail(form)

    def subscribe(self, email, code):
        try:
            logger.info('subscribing to GovDelivery')
            gd = GovDelivery(account_code=settings.ACCOUNT_CODE)

            subscription_response = gd.set_subscriber_topics(
                email_address=email,
                topic_codes=[code]
            )

            subscription_response.raise_for_status()
        except Exception:
            logger.exception('error subscribing to GovDelivery')
        else:
            return True

        messages.error(
            self.request,
            'There was an error in your submission. Please try again later.'
        )

        return False

    def success(self):
        if self.request.is_ajax():
            return JsonResponse({'result': 'pass'})
        else:
            messages.success(self.request,
                             'Your submission was successfully received.')
            return HttpResponseRedirect(self.page.url)

    def fail(self, form):
        if self.request.is_ajax():
            return JsonResponse({'result': 'fail'})

        else:
            for field, errors in form.errors.iteritems():
                for message in errors:
                    messages.error(self.request, message)

            return {'form': form}
