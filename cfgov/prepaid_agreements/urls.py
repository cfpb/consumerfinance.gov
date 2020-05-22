from prepaid_agreements.views import detail, index


try:
    from django.urls import re_path
except ImportError:
    from django.conf.urls import url as re_path


urlpatterns = [
    re_path(r"^$", index, name="index"),
    re_path(r"^detail/(?P<product_id>\d+)/$", detail, name="detail"),
]
