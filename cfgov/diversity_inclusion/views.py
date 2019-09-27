from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from diversity_inclusion.forms import VoluntaryAssessmentForm


class GetAssessmentForm(TemplateView):
    # if this is a POST request we need to process the form data
    def post(self, request):
        # create a form instance and populate it with data from the request:
        form = VoluntaryAssessmentForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('form_submitted'))

    # if a GET (or any other method) we'll create a blank form
    def get(self, request):
        form = VoluntaryAssessmentForm()
        return render(
            request,
            'diversity_inclusion/voluntary-assessment-form.html',
            {'form': form}
        )
