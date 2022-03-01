from django.views.generic import TemplateView


class CCDBSearchView(TemplateView):
    """Consumer Complaint Database search page view.

    This view renders the template for the CCDB search application page.
    """

    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        response["Edge-Cache-Tag"] = "complaints"
        return response

    template_name = "ccdb-complaint/ccdb-search.html"
