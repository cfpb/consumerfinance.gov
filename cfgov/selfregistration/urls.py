from django.conf.urls import patterns, url

from .views import Export

urlpatterns = patterns('selfregistration.views',
                       # Examples:
                       url(r'^export/', Export.as_view(),
                           name="export_registrations"),
                       )
