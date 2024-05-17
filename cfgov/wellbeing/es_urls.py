from core.views import TranslatedTemplateView
from wellbeing.views import ResultsView


try:
    from django.urls import re_path
except ImportError:
    from django.conf.urls import url as re_path


urlpatterns = [
    re_path(
        r"^$",
        TranslatedTemplateView.as_view(
            template_name="wellbeing/home.html", language="es"
        ),
        name="fwb_home_es",
    ),
    re_path(
        r"^resultados/$",
        ResultsView.as_view(language="es"),
        name="fwb_results_es",
    ),
    re_path(
        r"^mas-sobre/$",
        TranslatedTemplateView.as_view(
            template_name="wellbeing/about.html", language="es"
        ),
        name="fwb_about_es",
    ),
    re_path(
        r"^error/$",
        TranslatedTemplateView.as_view(
            template_name="wellbeing/error.html", language="es"
        ),
        name="fwb_error_es",
    ),
]
