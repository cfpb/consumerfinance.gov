from django.views.generic import TemplateView

from flags.state import flag_enabled


class ComplaintLandingView(TemplateView):
    """Consumer Complaint Database landing page view.

    This view renders the template for the CCDB landing page.

    That template includes a hardcoded value for percent of timely complaint
    responses, which is currently 98%.

    It also displays a warning banner if a trouble feature flag has been set.
    """

    template_name = 'ccdb-complaint/complaint-landing.html'

    def get_context_data(self, **kwargs):
        context = super(ComplaintLandingView, self).get_context_data(**kwargs)

        context.update({
            'technical_issues': flag_enabled('CCDB_TECHNICAL_ISSUES'),
        })

        return context

    def dispatch(self, *args, **kwargs):
        response = super(ComplaintLandingView, self).dispatch(*args, **kwargs)
        response['Edge-Cache-Tag'] = 'complaints'
        return response


class CCDBSearchView(TemplateView):
    """Consumer Complaint Database search page view.

    This view renders the template for the CCDB search application page.
    """

    def dispatch(self, *args, **kwargs):
        response = super(CCDB5SearchView, self).dispatch(*args, **kwargs)
        response['Edge-Cache-Tag'] = 'complaints'
        return response

    template_name = 'ccdb-complaint/ccdb-search.html'
