from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import JsonResponse, HttpResponseRedirect
from wagtail.wagtailcore.blocks.stream_block import StreamValue

from .. import Handler
from v1.forms import FeedbackForm


class FeedbackHandler(Handler):
    def __init__(self, page, request, block_value):
        super(FeedbackHandler, self).__init__(page, request)
        self.block_value = block_value

    def process(self, is_submitted):
        if is_submitted:
            form = FeedbackForm(self.request.POST)
            return self.get_response(form)

        return {'form': FeedbackForm()}

    def get_response(self, form):
        if form.is_valid():
            feedback = form.save(commit=False)
            is_helpful = self.request.POST.get('is_helpful', None)
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
            else:
                message = 'Something went wrong. Please try again.'
                messages.error(self.request, message)

        return {'form': form}
