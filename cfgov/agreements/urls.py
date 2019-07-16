from django.conf.urls import url

from agreements.views import index, issuer_search, prepaid, detail


urlpatterns = [
    url(r'^$', prepaid, name='prepaid'),
    url(r'^detail/$', detail, name='detail'),
    url(r'^$', index, name='agreements_home'),
    url(r'^issuer/(?P<issuer_slug>.*)/$',
        issuer_search,
        name='issuer_search'),
]
