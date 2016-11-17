from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect

from .. import Handler
from v1.forms import (
    FeedbackForm,
    ReferredFeedbackForm,
    SuggestionFeedbackForm
)

FEEDBACK_TYPES = {
    'helpful': FeedbackForm,
    'referred': ReferredFeedbackForm,
    'suggestion': SuggestionFeedbackForm
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

    def process(self, is_submitted):

        form_cls = FEEDBACK_TYPES[get_feedback_type(self.block_value)]

        if is_submitted:
            form = form_cls(self.request.POST)
            return self.get_response(form)

        return {'form': form_cls()}

    def get_response(self, form):
        if form.is_valid():
            feedback = form.save(commit=False)
            is_helpful = self.request.POST.get('is_helpful', None)
            if is_helpful is not None:
                feedback.is_helpful = bool(int(is_helpful))
            feedback.page = self.page
            feedback.save()
            return self.success()
        else:
            return self.fail(form)

    def success(self):
        if self.request.is_ajax():
            return JsonResponse({'result': 'pass'})
        else:
            messages.success(self.request, message='Thanks for your feedback!')
            return HttpResponseRedirect(self.page.url)

    def fail(self, form):
        if self.request.is_ajax():
            return JsonResponse({'result': 'fail'})

        else:
            if form.errors.get('is_helpful', None):
                messages.error(self.request, 'You must select an option.')
            elif form.errors.get('comment', None):
                messages.error(self.request, 'You must enter a comment.')
            else:
                message = 'Something went wrong. Please try again.'
                messages.error(self.request, message)

        return {'form': form}
