from django.conf.urls import url, patterns


urlpatterns = patterns(
    'cal.views',
    url(r'^$', 'display', name='leadership-calendar'),
    url(r'^pdf/$',
        'display',
        kwargs={'pdf': True},
        name='leadership-calendar-pdf'),
)
