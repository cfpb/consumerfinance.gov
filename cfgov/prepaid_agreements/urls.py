from django.urls import re_path

from prepaid_agreements.views import detail, index


urlpatterns = [
    re_path(r"^$", index, name="index"),
    re_path(r"^detail/(?P<product_id>\d+)/$", detail, name="detail"),
]
