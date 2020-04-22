from django.urls import re_path
from django.views.generic import TemplateView

from wellbeing.views import ResultsView


urlpatterns = [
    re_path(
        r"^$(?i)",
        TemplateView.as_view(template_name="wellbeing/home.html"),
        name="fwb_home",
    ),
    re_path(r"^results/$(?i)", ResultsView.as_view(), name="fwb_results"),
    re_path(
        r"^about/$(?i)",
        TemplateView.as_view(template_name="wellbeing/about.html"),
        name="fwb_about",
    ),
]
