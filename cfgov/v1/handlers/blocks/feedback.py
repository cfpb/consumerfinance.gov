# -*- coding: utf-8 -*-

from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse

from v1.forms import FeedbackForm, ReferredFeedbackForm, SuggestionFeedbackForm
from v1.handlers import Handler


FEEDBACK_TYPES = {
    "helpful": FeedbackForm,
    "referred": ReferredFeedbackForm,
    "suggestion": SuggestionFeedbackForm,
}

THANKS_MAP = {
    "en": "Thanks for your feedback!",
    "es": "\xa1Gracias por tus comentarios!",
}


def get_feedback_type(block_value):
    if block_value:
        if block_value.get("was_it_helpful_text"):
            return "helpful"
        elif block_value.get("radio_intro"):
            return "suggestion"
        else:
            return "referred"
    else:
        return "helpful"


class FeedbackHandler(Handler):
    def __init__(self, page, request, block_value):
        super().__init__(page, request)
        self.block_value = block_value

    def sanitize_referrer(self):
        """Skip referrer URLs that fail to encode or decode."""
        referrer = self.request.META.get("HTTP_REFERER", "")
        try:
            referrer.encode("utf8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            referrer = ""
        return referrer

    def process(self, is_submitted):
        form_cls = FEEDBACK_TYPES[get_feedback_type(self.block_value)]

        if is_submitted:
            form = form_cls(self.request.POST)
            return self.get_response(form)

        return {"form": form_cls(), "referrer": self.sanitize_referrer()}

    def get_response(self, form):
        if form.is_valid():
            feedback = form.save(commit=False)
            try:
                feedback.is_helpful = bool(int(self.request.POST.get("is_helpful")))
            except (ValueError, TypeError):
                pass

            # The referrer is set manually here instead of being set on the
            # ModelForm. Whereas MySQL silently truncates varchar fields that
            # exceed the column length, Postgres does not and will raise a
            # "value too long for type character varying" error if an
            # excessively long referrer is saved.
            #
            # This code grabs the referrer from the request and truncates it
            # to at most the length of the feedback model referrer field.
            referrer = self.request.POST.get("referrer", "")
            referrer_field = feedback._meta.get_field("referrer")
            referrer_max_length = referrer_field.max_length
            feedback.referrer = referrer[:referrer_max_length]

            feedback.page = self.page
            feedback.save()
            return self.success()
        else:
            return self.fail(form)

    def success(self):
        if self.request.is_ajax():
            if get_feedback_type(self.block_value) == "suggestion":
                return JsonResponse(
                    {
                        "result": "pass",
                        "heading": "Thank you!",
                        "message": "Be sure to also sign up for our email list "
                        "to get our blog posts and other tips about homebuying "
                        "and mortgages in your inbox. We'll also let you know "
                        "when we make updates to Buying a House.",
                    }
                )
            else:
                return JsonResponse(
                    {
                        "result": "pass",
                        "heading": "",
                        "message": THANKS_MAP[self.page.language],
                    }
                )
        else:
            messages.success(self.request, message=THANKS_MAP[self.page.language])
            return HttpResponseRedirect(self.request.path)

    def fail(self, form):
        if form.errors.get("is_helpful", None):
            msg = "You must select an option."
        elif form.errors.get("comment", None):
            msg = "You must enter a comment."
        elif form.errors.get("email", None):
            msg = "You must enter a valid email."
        else:
            msg = "Something went wrong. Please try again."

        if self.request.is_ajax():
            return JsonResponse({"result": "fail", "message": msg})
        else:
            messages.error(self.request, msg)
            return {"form": form}
