from retirement_api.views import about, claiming, estimator


try:
    from django.urls import re_path
except ImportError:
    from django.conf.urls import url as re_path


app_name = "retirement_api"

urlpatterns = [
    re_path(r"^before-you-claim/about/$", about, name="about"),
    re_path(
        r"^before-you-claim/about/es/$",
        about,
        {"language": "es"},
        name="about_es",
    ),
    re_path(r"^before-you-claim/$", claiming, name="claiming"),
    re_path(
        r"^before-you-claim/es/$", claiming, {"es": True}, name="claiming_es"
    ),
    re_path(
        r"^retirement-api/estimator/(?P<dob>[^/]+)/(?P<income>\d+)/$",
        estimator,
        name="estimator",
    ),
    re_path(
        r"^retirement-api/estimator/(?P<dob>[^/]+)/(?P<income>\d+)/es/$",
        estimator,
        {"language": "es"},
        name="estimator_es",
    ),
]
