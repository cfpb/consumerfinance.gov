from django.conf.urls import patterns, include, url

from .views import Export

urlpatterns = patterns('selfregistration.views',
    # Examples:
    url(r'^export/', Export.as_view(), name="export_registrations"),
)
