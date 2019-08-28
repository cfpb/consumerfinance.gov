from django.conf.urls import url

from prepaid_agreements.views import index, detail


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^detail/(?P<product_id>\d+)/$', detail, name='detail'),
]
