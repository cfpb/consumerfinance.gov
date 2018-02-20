# -*- coding: utf-8 -*-
import urllib

from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse

from v1.forms import FeedbackForm, ReferredFeedbackForm, SuggestionFeedbackForm

from .. import Handler


FEEDBACK_TYPES = {
    'helpful': FeedbackForm,
    'referred': ReferredFeedbackForm,
    'suggestion': SuggestionFeedbackForm
}

THANKS_MAP = {
    'en': 'Thanks for your feedback!',
    'es': '¡Gracias por tus comentarios!'
}


def get_feedback_type(block_value):
    if block_value:
        if block_value.get('was_it_helpful_text'):
            return 'helpful'
        elif block_value.get('radio_intro'):
            return 'suggestion'
        else:
            return 'referred'
    else:
        return 'helpful'


class FeedbackHandler(Handler):
    def __init__(self,
                 page,
                 request,
                 block_value):
        super(FeedbackHandler, self).__init__(page, request)
        self.block_value = block_value

    def sanitize_referrer(self):
        known_miscodings = {
            u'\xc3\xb3': u'\xf3',
            u'\xc3\xa9': u'\xe9',
            u'\xc3\xad': u'\xed',
        }
        referrer = self.request.META.get('HTTP_REFERER', '')
        try:
            referrer.encode('ascii')
        except (UnicodeEncodeError):
            for char in known_miscodings:
                referrer = referrer.replace(char, known_miscodings[char])
            referrer = urllib.quote(referrer.encode('utf8'), safe=':/')
        return referrer

    def process(self, is_submitted):
        form_cls = FEEDBACK_TYPES[get_feedback_type(self.block_value)]

        if is_submitted:
            form = form_cls(self.request.POST)
            return self.get_response(form)

        self.block_value.update({'referrer': self.sanitize_referrer()})
        return {'form': form_cls()}

    def get_response(self, form):
        if form.is_valid():
            feedback = form.save(commit=False)
            try:
                feedback.is_helpful = bool(
                    int(self.request.POST.get('is_helpful'))
                )
            except (ValueError, TypeError):
                pass
            feedback.referrer = self.request.POST.get('referrer', '')
            feedback.page = self.page
            feedback.save()
            return self.success()
        else:
            return self.fail(form)

    def success(self):
        if self.request.is_ajax():
            if get_feedback_type(self.block_value) == 'suggestion':
                return JsonResponse(
                    {'result': 'pass',
                     'heading': 'Thank you!',
                     'message': "Be sure to also sign up for our email list "
                     "to get our blog posts and other tips about homebuying "
                     "and mortgages in your inbox. We'll also let you know "
                     "when we make updates to Owning a Home."}
                )
            else:
                return JsonResponse(
                    {'result': 'pass',
                     'heading': '',
                     'message': THANKS_MAP[self.page.language]}
                )
        else:
            messages.success(
                self.request, message=THANKS_MAP[self.page.language])
            return HttpResponseRedirect(self.request.path)

    def fail(self, form):
        if form.errors.get('is_helpful', None):
            msg = 'You must select an option.'
        elif form.errors.get('comment', None):
            msg = 'You must enter a comment.'
        elif form.errors.get('email', None):
            msg = 'You must enter a valid email.'
        else:
            msg = 'Something went wrong. Please try again.'

        if self.request.is_ajax():
            return JsonResponse({'result': 'fail', 'message': msg})
        else:
            messages.error(self.request, msg)
            return {'form': form}
