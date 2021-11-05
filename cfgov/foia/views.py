from django.urls import reverse_lazy
from django.views.generic import FormView

from foia.forms import DisclosureConsentForm, RecordsAccessForm


class GetDisclosureConsentForm(FormView):
    template_name = 'foia/disclosure-consent-form.html'
    form_class = DisclosureConsentForm
    success_url = reverse_lazy('foia:foia_form_submitted')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super(GetDisclosureConsentForm, self).form_valid(form)

class GetRecordsAccessForm(FormView):
    template_name = 'foia/records-access-form.html'
    form_class = RecordsAccessForm
    success_url = reverse_lazy('foia:foia_form_submitted')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super(GetRecordsAccessForm, self).form_valid(form)
