import json
from govdelivery.api import GovDelivery
from urlparse import urlparse

from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse

from v1.handlers import Handler
from .forms import ConferenceRegistrationForm


class ConferenceRegistrationHandler(Handler):
    def __init__(self, page, request, block_value):
        super(ConferenceRegistrationHandler, self).__init__(page, request)
        self.block_value = block_value

    def process(self, is_submitted):
        if is_submitted:
            data = self.get_post_data()
            form = ConferenceRegistrationForm(data)
            response = self.process_form(form)
            if response:
                return response

        return {'form': ConferenceRegistrationForm()}

    def get_post_data(self):
        data = self.request.POST.copy()
        sessions = self.request.POST.getlist('form_sessions', [])
        data['sessions'] = ','.join(sessions)
        return data

    def process_form(self, form):
        if form.is_valid():
            attendee = form.save(commit=False)
            codes = self.request.POST.getlist('codes', [])

            if self.subscribe(attendee.email, codes):
                self.save_attendee(attendee)
                return self.success()

        return self.fail(form)

    def subscribe(self, email, codes):
        message = 'The subscription failed. Please try again later.'
        try:
            gd = GovDelivery(account_code=settings.ACCOUNT_CODE)
            subscription_response = gd.set_subscriber_topics(email, codes)
            if subscription_response.status_code != 200:
                messages.error(self.request, message=message)
                return False
        except (KeyError, Exception):
            messages.error(self.request, message=message)
            return False

        return True

    def save_attendee(self, attendee):
        attendee.sessions = json.dumps(self.get_sessions())
        attendee.save()

    def get_sessions(self):
        ids = self.request.POST.getlist('form_sessions', [])
        sessions = self.block_value.get('sessions', [])
        return [session for i, session in enumerate(sessions) if str(i) in ids]

    def success(self):
        if self.request.is_ajax():
            return JsonResponse({'result': 'pass'})
        else:
            message = 'Your registration is complete!'
            messages.success(self.request, message=message)

    def fail(self, form):
        if self.request.is_ajax():
            return JsonResponse({'result': 'fail'})
        else:
            for errors in form.errors.values():
                for error in errors:
                    messages.error(self.request, message=error)
            return {'form': form}
