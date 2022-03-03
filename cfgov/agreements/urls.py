try:
    from django.urls import re_path
except ImportError:
    from django.conf.urls import url as re_path

from agreements.views import index, issuer_search

urlpatterns = [
    re_path(r"^$", index, name="agreements_home"),
    re_path(
        r"^issuer/(?P<issuer_slug>.*)/$", issuer_search, name="issuer_search"
    ),
]
