from django.urls import reverse_lazy
from django.views.generic import FormView

from diversity_inclusion.forms import VoluntaryAssessmentForm


class GetAssessmentForm(FormView):
    template_name = "diversity_inclusion/voluntary-assessment-form.html"
    form_class = VoluntaryAssessmentForm
    success_url = reverse_lazy("diversity_inclusion:form_submitted")

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)
