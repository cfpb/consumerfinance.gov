from django.conf.urls import *

urlpatterns = patterns('',
    url(r'(?P<year>\d{4})/(?P<month>.*)/$', 'cal.views.display_html'),
    url(r'cfpb-leadership.ics$', 'cal.views.display_ics'),
    url(r'cfpb-leadership.rss$', 'cal.views.display_rss'),
    url(r'^$', 'cal.views.display_html'),
)
