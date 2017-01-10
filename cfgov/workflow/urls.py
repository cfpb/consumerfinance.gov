from django.conf.urls import url

from workflow.views import migrate

urlpatterns = [
    url(r'^(\d+)/migrate/(\d+)/$', migrate, name='migrate_to_site'),
]
