from django.conf.urls import url

from agreements.views import index, issuer_search


urlpatterns = [
    url(r'^$', index, name='agreements_home'),
    url(r'^issuer/(?P<issuer_slug>.*)/$',
        issuer_search,
        name='issuer_search'),
]
