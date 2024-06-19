from core.views import TranslatedTemplateView
from wellbeing.views import ResultsView


try:
    from django.urls import re_path
except ImportError:
    from django.conf.urls import url as re_path


urlpatterns = [
    re_path(
        r"^$",
        TranslatedTemplateView.as_view(template_name="wellbeing/home.html"),
        name="fwb_home_en",
    ),
    re_path(r"^results/$", ResultsView.as_view(), name="fwb_results_en"),
    re_path(
        r"^about/$",
        TranslatedTemplateView.as_view(template_name="wellbeing/about.html"),
        name="fwb_about_en",
    ),
    re_path(
        r"^error/$",
        TranslatedTemplateView.as_view(template_name="wellbeing/error.html"),
        name="fwb_error_en",
    ),
]
