from django.views.generic import TemplateView

from flags.state import flag_enabled


class ComplaintLandingView(TemplateView):
    """Consumer Complaint Database landing page view.

    This view renders the template for the CCDB landing page.

    That template includes a hardcoded value for percent of timely complaint
    responses, which is currently 98%.

    It also displays a warning banner if a trouble feature flag has been set.
    """

    template_name = 'complaint/complaint-landing.html'

    def get_context_data(self, **kwargs):
        context = super(ComplaintLandingView, self).get_context_data(**kwargs)

        context.update({
            'technical_issues': flag_enabled('CCDB_TECHNICAL_ISSUES'),
        })

        return context
