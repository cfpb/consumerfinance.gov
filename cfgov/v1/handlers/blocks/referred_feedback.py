from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect

from .. import Handler
from v1.forms import ReferredFeedbackForm


class ReferredFeedbackHandler(Handler):
    def __init__(self, page, request, block_value):
        super(ReferredFeedbackHandler, self).__init__(page, request)
        self.block_value = block_value

    def process(self, is_submitted):
        if is_submitted:
            form = ReferredFeedbackForm(self.request.POST)
            return self.get_response(form)

        return {'form': ReferredFeedbackForm()}

    def get_response(self, form):
        if form.is_valid():
            feedback = form.save(commit=False)
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
            if form.errors.get('comment', None):
                messages.error(self.request, 'You must enter a comment.')
            else:
                message = 'Something went wrong. Please try again.'
                messages.error(self.request, message)

        return {'form': form}
