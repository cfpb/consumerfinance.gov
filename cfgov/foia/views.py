from django.urls import reverse_lazy
from django.views.generic import FormView

from foia.forms import FoiaRequestForm


class GetRequestForm(FormView):
    template_name = 'foia/foia-request-form.html'
    form_class = FoiaRequestForm
    success_url = reverse_lazy('foia:foia_form_submitted')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super(GetRequestForm, self).form_valid(form)
