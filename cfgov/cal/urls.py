from django.conf.urls import *


urlpatterns = patterns('cal.views',
    url(r'^$', 'display'),
    url(r'^pdf/$',
        'display',
        kwargs={'pdf':True},
        name='leadership-calendar-pdf'),
)
