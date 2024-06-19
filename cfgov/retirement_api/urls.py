from core.views import TranslatedTemplateView
from retirement_api.views import estimator


try:
    from django.urls import re_path
except ImportError:
    from django.conf.urls import url as re_path

app_name = "retirement_api_en"

urlpatterns = [
    re_path(
        r"^before-you-claim/about/$",
        TranslatedTemplateView.as_view(
            template_name="retirement_api/about.html", language="en"
        ),
        name="about",
    ),
    re_path(
        r"^before-you-claim/$",
        TranslatedTemplateView.as_view(
            template_name="retirement_api/claiming.html", language="en"
        ),
        name="claiming",
    ),
    re_path(
        r"^retirement-api/estimator/(?P<dob>[^/]+)/(?P<income>\d+)/$",
        estimator,
        name="estimator",
    ),
]
